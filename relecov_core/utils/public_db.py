import relecov_core.models
import relecov_core.utils.plotly_graphics


def get_public_accession_from_sample_lab(p_field, sample_objs=None):
    """Get the list of the accesion values with their sample.
    If not samples are given it gets the information for all samples
    """
    if sample_objs is None:
        return relecov_core.models.PublicDatabaseValues.objects.filter(
            public_database_fieldID__property_name__exact=p_field,
            value__icontains="EPI_ISL",
        ).values_list(
            "sampleID__collecting_institution",
            "sampleID__sequencing_sample_id",
            "value",
        )
    else:
        return relecov_core.models.PublicDatabaseValues.objects.filter(
            sampleID__in=sample_objs,
            public_database_fieldID__property_name__exact=p_field,
            value__icontains="EPI_ISL",
        ).values_list("sampleID__sequencing_sample_id", "value")


def percentage_graphic(len_sample, len_acc, title):
    """Display Pie graphic with upload samples as len_acc and not upload as the
    difference from total sample minus the ones that are uploaded
    """
    data = [len_acc, len_sample - len_acc]
    names = ["Upload", "Pending"]
    return relecov_core.utils.plotly_graphics.pie_graphic(data, names, title)


def get_public_information_from_sample(p_type, sample_id):
    """Return all values that are stored for the sample and for the public type"""
    if relecov_core.models.PublicDatabaseValues.objects.filter(
        sampleID__pk=sample_id,
        public_database_fieldID__database_type__public_type_name__iexact=p_type,
    ).exists():
        return relecov_core.models.PublicDatabaseValues.objects.filter(
            sampleID__pk=sample_id,
            public_database_fieldID__database_type__public_type_name__iexact=p_type,
        ).values_list("public_database_fieldID__label_name", "value")
    return []
