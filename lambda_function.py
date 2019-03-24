from domain_response import Success, DomainException, InternalError
from domain_pre_signed import Domain
import boto3


s3 = boto3.client('s3')


def generate_presigned_url_for_upload(domain):
    """

    :param domain:
    :return:
    """
    params = {'Bucket': domain.bucket, 'Key': domain.key}
    if domain.is_content_type():
        params['ContentType'] = domain.content_type

    return s3.generate_presigned_url(
        ClientMethod='put_object',
        Params=params,
        ExpiresIn=domain.expire,
        HttpMethod=domain.method)


def lambda_handler(event, context):
    """

    :param event:
    :param context:
    :return:
    """
    try:
        domain = Domain(event)
        uri = generate_presigned_url_for_upload(domain)
        return Success(uri).to_json()
    except DomainException as ex:
        return ex.to_json()
    except Exception as ex:
        return InternalError().to_json()

