import os
import pdfkit


def html_to_pdf(html_string: str, output_path=False):
    config = pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_PATH'))
    if not output_path:
        return pdfkit.from_string(html_string, configuration=config)
    else:
        return pdfkit.from_string(html_string, configuration=config, output_path='./report.pdf')
