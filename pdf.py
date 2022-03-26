import os
import pdfkit


def html_to_pdf(html_string: str):
    config = pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_PATH'))
    return pdfkit.from_string(html_string, configuration=config)
