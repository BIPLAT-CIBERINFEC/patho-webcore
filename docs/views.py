# Generic imports
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Local imports
import docs.utils.markdown


@login_required
def index(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("index.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def description(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("description.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def relecov_install(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("relecov_install.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def configuration(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("configuration.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def metadata(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("metadata.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def metadata_lab_excel(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("metadata_lab_excel.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def relecov_tools(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("relecov_tools.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def intranet_overview(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("intranet_overview.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def intranet_contact_data(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("intranet_contact_data.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def intranet_sample_search(request):
    converted_to_html = docs.utils.markdown.markdown_to_html(
        "intranet_sample_search.md"
    )
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def intranet_received_samples(request):
    converted_to_html = docs.utils.markdown.markdown_to_html(
        "intranet_received_samples.md"
    )
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def intranet_upload_metadata(request):
    converted_to_html = docs.utils.markdown.markdown_to_html(
        "intranet_upload_metadata.md"
    )
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def variant_dashboard(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("variant_dashboard.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def methodology_dashboard(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("methodology_dashboard.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def nextstrain_install(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("nextstrain_install.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def howto_nextstrain(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("howto_nextstrain.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def upload_to_ena(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("upload_to_ena.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def upload_to_gisaid(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("upload_to_gisaid.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def upload_metadata(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("upload_metadata.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def api_schema(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("api_schema.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def howto_api(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("howto_api.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )


@login_required
def create_new_user(request):
    converted_to_html = docs.utils.markdown.markdown_to_html("create_new_user.md")
    if isinstance(converted_to_html, dict):
        return render(request, "docs/error_404.html")
    converted_to_html = docs.utils.markdown.fix_img_folder(converted_to_html)
    return render(
        request,
        "docs/base.html",
        {"html": converted_to_html},
    )
