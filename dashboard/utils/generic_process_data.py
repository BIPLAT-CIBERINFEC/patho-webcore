# Generic imports
from datetime import datetime

# Local imports
import core.models
import core.utils.lineage
import core.utils.variants
import core.utils.rest_api
import dashboard.models


def pre_proc_calculation_date():
    """Fetch the information about date for each sample to know about the
    number of days between different steps of samples
    """

    def convert_data_to_sample_dict(data, data_1, data_2):
        out_data = {}
        for item in data:
            if item[data_1] not in out_data:
                out_data[item[data_1]] = item[data_2]
        return out_data

    def convert_str_to_datetime(data, separator, invalid_samples):
        """Convert the string values to datetime object to perform calculation
        dates
        """
        # start_date is set to discard not valid dates, because they were
        # mistyped by user
        start_date = datetime.strptime("2019-12-31", "%Y-%m-%d")
        if separator:
            d_format = "%Y" + separator + "%m" + separator + "%d"
        else:
            d_format = "%Y%m%d"
        for sample in data.keys():
            if sample in invalid_samples:
                continue
            if sample == "Not Provided [GENEPIO:0001668]":
                continue
            if data[sample]:
                f_date = datetime.strptime(data[sample], d_format)
                if f_date < start_date:
                    invalid_samples[sample] = True
                else:
                    data[sample] = f_date
        return data, invalid_samples

    def calculate_days(sample_list, date_1, date_2):
        """Function gets 2 dictionary lists. For the same sample the subtract
        operation date_2 - date_1 is done.
        """
        out_data = []
        for sample in sample_list:
            if sample in date_1 and sample in date_2:
                try:
                    days = (date_2[sample] - date_1[sample]).days
                    if (date_2[sample] - date_1[sample]).days > 1000:
                        print(sample, "numero dias ", days)
                    out_data.append((date_2[sample] - date_1[sample]).days)
                except TypeError:
                    out_data.append("bbbb")
            else:
                out_data.append("aaaaaa")
        return out_data

    # get sequencing date from sample table
    invalid_samples = {}
    analysis_date = core.models.BioinfoAnalysisValue.objects.filter(
        bioinfo_analysis_fieldID__property_name__exact="analysis_date",
    ).values("value", "sample__collecting_lab_sample_id")
    analysis_date = convert_data_to_sample_dict(
        analysis_date, "sample__collecting_lab_sample_id", "value"
    )
    analysis_date, invalid_samples = convert_str_to_datetime(
        analysis_date, None, invalid_samples
    )

    seq_date = core.models.Sample.objects.all().values(
        "collecting_lab_sample_id", "sequencing_date"
    )
    seq_date = convert_data_to_sample_dict(
        seq_date, "collecting_lab_sample_id", "sequencing_date"
    )

    # send request to iSkyLIMS
    collection_date = core.utils.rest_api.get_sample_parameter_data(
        "collection_sample_date"
    )
    collection_date = convert_data_to_sample_dict(
        collection_date, "Sample Name", "collection_sample_date"
    )
    collection_date, invalid_samples = convert_str_to_datetime(
        collection_date, "-", invalid_samples
    )

    recorded_date = core.utils.rest_api.get_sample_parameter_data("sample_entry_date")
    recorded_date = convert_data_to_sample_dict(
        recorded_date, "Sample Name", "sample_entry_date"
    )
    recorded_date, invalid_samples = convert_str_to_datetime(
        recorded_date, "-", invalid_samples
    )

    # perform calculation dates
    calculation_dates = {}
    sample_list = []
    for sam in seq_date.keys():
        if sam not in invalid_samples:
            sample_list.append(sam)

    # calculation_dates["samples"] = sample_list
    calculation_dates["coll_rec_date"] = calculate_days(
        sample_list, collection_date, recorded_date
    )
    calculation_dates["rec_seq_date"] = calculate_days(
        sample_list, recorded_date, seq_date
    )
    calculation_dates["seq_analyis_date"] = calculate_days(
        sample_list, seq_date, analysis_date
    )
    # json_data = json.dumps(calculation_dates)
    # Save json in database
    dashboard.models.GraphicJsonFile.objects.create_new_graphic_json(
        {"graphic_name": "calculation_date", "graphic_data": calculation_dates}
    )

    return {"SUCCESS": "Success"}


def pre_proc_variant_graphic():
    """Collect the variant information to store them at the pre-processed
    GraphicJsonFile. Smoothing is performed before saving into database
    """

    in_date_samples = core.utils.rest_api.fetch_samples_on_condition(
        "collection_sample_date"
    )
    if "ERROR" in in_date_samples:
        return in_date_samples

    date_sample = {}
    date_variant = {}
    for s_data in in_date_samples["DATA"]:
        if s_data["collection_sample_date"] not in date_sample:
            date_sample[s_data["collection_sample_date"]] = []
        date_sample[s_data["collection_sample_date"]].append(s_data["Sample Name"])

    for date, samples in date_sample.items():
        variant_samples = (
            core.models.LineageValues.objects.filter(
                lineage_fieldID__property_name="variant_name",
                sample__collecting_lab_sample_id__in=samples,
            )
            .values_list("value", flat=True)
            .distinct()
        )
        if len(variant_samples) == 0:
            continue
        if date not in date_variant:
            date_variant[date] = {}

        date_samples = 0
        for variant_name in variant_samples:
            if variant_name == "":
                continue

            if variant_name not in date_variant[date]:
                num_samples = core.models.Sample.objects.filter(
                    collecting_lab_sample_id__in=samples,
                    lineage_values__value__iexact=variant_name,
                ).count()
                date_variant[date][variant_name] = num_samples

            date_samples += num_samples
        # Discard the variants that the number of the samples are lower than
        # 5% for the total number of the samples collected from a specific date
        min_num_samples = date_samples / 20
        for v_name, number in date_variant[date].items():
            key_to_delete = []
            if number < min_num_samples:
                key_to_delete.append(v_name)
        # Delete the entry date if no variant name was identified for this
        # date
        if len(date_variant[date]) == 0:
            date_variant.pop(date, None)
            continue
        # Delete the variants where the number of samples is below the minimum
        # number of samples.
        for key in key_to_delete:
            date_variant[date].pop(key, None)

    # convert dictionary to list date, variant and samples to store in json
    # for reading later as table to create the dataframe
    collect_data = []
    num_samples_data = []
    variant_names = []
    for date_key, values in date_variant.items():
        for variant_key, value in values.items():
            collect_data.append(date_key)
            variant_names.append(variant_key)
            num_samples_data.append(value)
    variant_var_data = {
        "Collection date": collect_data,
        "Lineage": variant_names,
        "samples": num_samples_data,
    }
    json_data = {
        "graphic_name": "variant_graphic_data",
        "graphic_data": variant_var_data,
    }
    dashboard.models.GraphicJsonFile.objects.create_new_graphic_json(json_data)

    return {"SUCCESS": "Success"}


def pre_proc_variations_per_lineage(chromosome=None):
    """Process variants per lineages"""

    lineage_data = {}

    # Grab lineages matching selected lineage
    for lineage in core.utils.lineage.get_lineages_list():
        mutation_data = {}
        list_of_af = []
        list_of_pos = []
        list_of_effects = []

        lineage_value_objs = core.models.LineageValues.objects.filter(
            value__iexact=lineage
        )
        # Query samples matching that lineage
        sample_objs = core.models.Sample.objects.filter(
            lineage_values__in=lineage_value_objs
        )
        number_samples_wlineage = core.models.Sample.objects.filter(
            lineage_values__in=lineage_value_objs
        ).count()
        # Query variants with AF>0.75 for samples matching desired lineage. TODO: get this from threshold AF in metadata bioinfo in db.
        variants = (
            core.models.VariantInSample.objects.filter(
                sampleID_id__in=sample_objs, af__gt=0.75
            )
            .values_list("variantID_id", flat=True)
            .distinct()
        )

        for variant in variants:
            number_samples_wmutation = (
                core.models.VariantInSample.objects.filter(
                    sampleID_id__in=sample_objs, variantID_id=variant
                )
                .values_list("sampleID_id", flat=True)
                .count()
            )
            mut_freq_population = number_samples_wmutation / number_samples_wlineage
            pos = core.models.VariantInSample.objects.filter(variantID_id=variant)[
                0
            ].get_pos()

            effects = (
                core.models.VariantAnnotation.objects.filter(variantID_id__pk=variant)
                .values_list("effectID_id__effect", flat=True)
                .last()
            )

            # Only display mutations with at lease 0.05 freq in population
            if mut_freq_population > 0.05:
                list_of_af.append(mut_freq_population)
                list_of_pos.append(pos)
                list_of_effects.append(effects)

        domains = core.utils.variants.get_domains_and_coordenates(chromosome)

        mutation_data["x"] = list_of_pos
        mutation_data["y"] = list_of_af
        mutation_data["mutationGroups"] = list_of_effects
        mutation_data["domains"] = domains
        mutation_data["SamplesWithLineage"] = number_samples_wlineage

        lineage_data[lineage] = mutation_data

    dashboard.models.GraphicJsonFile.objects.create_new_graphic_json(
        {"graphic_name": "variations_per_lineage", "graphic_data": lineage_data}
    )

    return {"SUCCESS": "Success"}


# preprocessing data for Sample processing dashboard
def pre_proc_specimen_source_pcr_1():
    """Collect the cts values when using pcr 1 and per specimen source"""
    lims_data = core.utils.rest_api.get_stats_data(
        {
            "sample_project_name": "Relecov",
            "project_field": "specimen_source,diagnostic_pcr_Ct_value_1",
        }
    )
    if "ERROR" in lims_data:
        return lims_data

    dashboard.models.GraphicJsonFile.objects.create_new_graphic_json(
        {"graphic_name": "specimen_source_pcr_1", "graphic_data": lims_data}
    )

    return {"SUCCESS": "Success"}


def pre_proc_extraction_protocol_pcr_1():
    """Collect the cts values when using pcr 1 and per specimen source"""
    lims_data = core.utils.rest_api.get_stats_data(
        {
            "sample_project_name": "Relecov",
            "project_field": "nucleic_acid_extraction_protocol,diagnostic_pcr_Ct_value_1",
        }
    )
    if "ERROR" in lims_data:
        return lims_data

    dashboard.models.GraphicJsonFile.objects.create_new_graphic_json(
        {"graphic_name": "extraction_protocol_pcr_1", "graphic_data": lims_data}
    )

    return {"SUCCESS": "Success"}


# preprocessing data for Sequencing dashboard
def pre_proc_library_kit_pcr_1():
    """Collect the cts values when using pcr 1 and per library preparation kit"""
    lims_data = core.utils.rest_api.get_stats_data(
        {
            "sample_project_name": "Relecov",
            "project_field": "library_preparation_kit,diagnostic_pcr_Ct_value_1",
        }
    )
    if "ERROR" in lims_data:
        return lims_data

    dashboard.models.GraphicJsonFile.objects.create_new_graphic_json(
        {"graphic_name": "library_kit_pcr_1", "graphic_data": lims_data}
    )

    return {"SUCCESS": "Success"}


def pre_proc_based_pairs_sequenced():
    based_pairs = {}
    pcr_ct_1_values = core.utils.rest_api.get_sample_parameter_data(
        {"sample_project_name": "relecov", "parameter": "diagnostic_pcr_Ct_value_1"}
    )
    if "ERROR" in pcr_ct_1_values:
        return pcr_ct_1_values
    for ct_value in pcr_ct_1_values:
        sample_name = ct_value["Sample name"]
        base_value = (
            core.models.BioinfoAnalysisValue.objects.filter(
                bioinfo_analysis_fieldID__property_name__exact="number_of_base_pairs_sequenced",
                sample__collecting_lab_sample_id__exact=sample_name,
            )
            .last()
            .get_value()
        )
        try:
            float_base_value = float(ct_value["diagnostic_pcr_Ct_value_1"])
            base_value_int = int(base_value)
        except ValueError:
            continue
        if base_value_int not in based_pairs:
            based_pairs[base_value_int] = []
        based_pairs[base_value_int].append(float_base_value)

    dashboard.models.GraphicJsonFile.objects.create_new_graphic_json(
        {
            "graphic_name": "ct_number_of_base_pairs_sequenced",
            "graphic_data": based_pairs,
        }
    )

    return {"SUCCESS": "Success"}


# data preparation for methodology bioinfo dashboard
def pre_proc_depth_variants():
    depth_sample_list = core.models.BioinfoAnalysisValue.objects.filter(
        bioinfo_analysis_fieldID__property_name__exact="depth_of_coverage_value"
    ).values("value", "sample__collecting_lab_sample_id")
    variant_sample_list = core.models.BioinfoAnalysisValue.objects.filter(
        bioinfo_analysis_fieldID__property_name__exact="number_of_variants_in_consensus"
    ).values("value", "sample__collecting_lab_sample_id")
    tmp_depth = {}
    depth_variant = {}
    for item in depth_sample_list:
        try:
            tmp_depth[item["sample__collecting_lab_sample_id"]] = float(item["value"])
        except ValueError:
            # ignore the entry if value cannot converted to float
            continue
    for item in variant_sample_list:
        # ignore the samples that do not have depth value
        if item["sample__collecting_lab_sample_id"] not in tmp_depth:
            continue
        d_value = float(tmp_depth[item["sample__collecting_lab_sample_id"]])
        if d_value not in depth_variant:
            depth_variant[d_value] = []
        depth_variant[d_value].append(int(item["value"]))
    # depth_variant_ordered = dict(sorted(depth_variant.items()))
    # depth.append(tmp_depth[item["sample__collecting_lab_sample_id"]])
    # variant.append(int(item["value"]))
    # depth_variant = {"depth": depth, "variant": variant}
    dashboard.models.GraphicJsonFile.objects.create_new_graphic_json(
        {
            "graphic_name": "depth_variant_consensus",
            "graphic_data": depth_variant,
        }
    )
    return {"SUCCESS": "Success"}


def pre_proc_depth_sample_run():
    depth_sample_list = core.models.BioinfoAnalysisValue.objects.filter(
        bioinfo_analysis_fieldID__property_name__exact="depth_of_coverage_value"
    ).values("value", "sample__collecting_lab_sample_id")
    if len(depth_sample_list) == 0:
        return {"ERROR": "No data"}
    sample_in_run = core.utils.rest_api.get_sample_parameter_data(
        {"sample_project_name": "relecov", "parameter": "number_of_samples_in_run"}
    )
    # return error, no connection to LIMS
    if "ERROR" in sample_in_run:
        return sample_in_run
    tmp_depth = {}
    depth_sample_run = {}
    for item in depth_sample_list:
        try:
            tmp_depth[item["sample__collecting_lab_sample_id"]] = float(item["value"])
        except ValueError:
            # ignore the entry if value cannot converted to float
            continue
    for item in sample_in_run:
        try:
            int(item["number_of_samples_in_run"])
        except ValueError:
            # ignore the entry if number_of_samples cannot converted to int
            continue
        if item["Sample name"] not in tmp_depth:
            continue
        d_value = tmp_depth[item["Sample name"]]
        if d_value not in depth_sample_run:
            depth_sample_run[d_value] = []
        depth_sample_run[d_value].append(int(item["number_of_samples_in_run"]))

    dashboard.models.GraphicJsonFile.objects.create_new_graphic_json(
        {
            "graphic_name": "depth_samples_in_run",
            "graphic_data": depth_sample_run,
        }
    )
    return {"SUCCESS": "Success"}
