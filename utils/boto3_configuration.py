import logging

import boto3
from botocore.exceptions import ClientError


class Boto3Configuration:
    def __init__(self, access_id, secret_key, region, bucket_name):
        self._logger = logging.getLogger(__name__)
        self._session = boto3.Session(aws_access_key_id=access_id,
                                      aws_secret_access_key=secret_key,
                                      region_name=region)
        self._bucket_name = bucket_name

    def upload_model_files(self):
        """
        This method upload model file into a S3 Bucket

        :return: True if file was uploaded, else False
        """

        s3 = self._session.resource('s3')
        bucket = s3.Bucket(self._bucket_name)

        try:
            bucket.upload_file("model.txt", "model.txt")
            self._logger.info("============ UPLOAD MODEL FILE COMPLETED ============")
            bucket.upload_file("scaler.pkl", "scaler.pkl")
            self._logger.info("============ UPLOAD Scaler FILE COMPLETED ============")

        except ClientError as e:
            logging.error(e)
            return False
        return True
