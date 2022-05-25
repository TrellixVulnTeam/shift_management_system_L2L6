import cdk = require('@aws-cdk/core');
import s3 = require('@aws-cdk/aws-s3');
import { DataSourceStackProps } from './data-source-stack'

export default class CreateBucketViewerWebsite {
  public static execute(stack: cdk.Stack, isDev: boolean, props: DataSourceStackProps): s3.Bucket {
    const bucket: s3.Bucket = new s3.Bucket(stack, `bucket-viewer-website-${props.isAdmin ? "admin" : "user"}${isDev ? "-dev" : ""}`, {
      blockPublicAccess: new s3.BlockPublicAccess({
        blockPublicAcls: true,
        blockPublicPolicy: true,
        ignorePublicAcls: true,
        restrictPublicBuckets: true
      }),
      bucketName: `${props.projectName}-viewer-website-${props.isAdmin ? "admin" : "user"}${isDev ? "-dev": ""}`,
      removalPolicy: cdk.RemovalPolicy.DESTROY, // cdk destroy時にバケットを消す
      encryption: s3.BucketEncryption.S3_MANAGED // 暗号化
    });
    return bucket
  }
}
