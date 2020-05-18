ALLOWED_EXTENSIONS = {'csv', 'json', 'vcf'}


def is_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
