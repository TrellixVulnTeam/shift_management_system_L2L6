import cdk = require('@aws-cdk/core');
import lambda = require("@aws-cdk/aws-lambda");
import iam = require('@aws-cdk/aws-iam');
import s3 = require("@aws-cdk/aws-s3");
import { ViewerStackProps } from './viewer-stack'

export default class CreateLambdaViewerApi {
  public static execute(
    stack: cdk.Stack,
    isStaging: boolean,
    bucketDataUser: s3.Bucket,
    bucketDataAdmin: s3.Bucket,
    bucketViewerWebsite: s3.Bucket,
    bucketViewerWebsiteDev: s3.Bucket,
    props: ViewerStackProps,
  ):lambda.Function  {

    var apiName = `ViewerAPI`
    var description = `Viewer API用lambda関数。`
    var debug = false
    var env = 'prod'
    var memorySize = 256
    if (isStaging) {
      apiName += `_staging`
      description += `[staging]`
      debug = true
      env = 'stg'
      memorySize = 128
    }

    const lambdaFunction: lambda.Function = new lambda.Function(stack, apiName, {
      runtime: lambda.Runtime.PYTHON_3_7,
      code: lambda.Code.fromAsset(`src/viewer/${props.isAdmin ? "admin" : "user"}/api`),
      handler: 'handler.lambda_handler',
      environment: {
        ACCOUNT_ID: props.accountId,
        PROJECT_NAME: props.projectName,
        VERSION: props.version,
        BUCKET_NAME_DATA_USER: bucketDataUser.bucketName,
        BUCKET_NAME_DATA_ADMIN: bucketDataAdmin.bucketName,
        DEST_S3_PREFIX: `shift`,
        DEST_S3_PREFIX_REGULAR_HOLIDAY: `regular_holiday`,
        DEBUG: debug ? 'true' : 'false',
        ENV: env,
        BUCKET_NAME_VIEWER_WEBSITE: bucketViewerWebsite.bucketName,
        BUCKET_NAME_VIEWER_WEBSITE_DEV: bucketViewerWebsiteDev.bucketName,
        VIEWER_WEBSITE_DOMAIN: props.distributionDomainName,
        VIEWER_WEBSITE_DOMAIN_DEV: props.distributionDomainNameDev,
        USER_POOL_ID: props.userPoolIdUser,
        USER_POOL_CLIENT_ID: props.userPoolClientIdUser,
        IS_ADMIN: props.isAdmin ? `true` : `false`,
      },
      functionName: `${props.projectName}-${apiName}-${props.isAdmin ? "admin" : "user"}-${props.version}`,
      description: `${description}-${props.isAdmin ? "admin" : "user"}-${props.version}`,
      memorySize: memorySize,
      timeout: cdk.Duration.minutes(3),
    })
    lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
      resources: [
        `${bucketDataUser.bucketArn}`,
        `${bucketDataUser.bucketArn}/*`,
      ],
      effect: iam.Effect.ALLOW,
      actions: [
        's3:GetObject',
        's3:PutObject',
        's3:PutObjectTagging',
        's3:ListBucket',
        's3:DeleteObject',
      ],
    }))
    lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
      resources: [
        `${bucketViewerWebsite.bucketArn}`,
        `${bucketViewerWebsite.bucketArn}/*`,
        `${bucketViewerWebsiteDev.bucketArn}`,
        `${bucketViewerWebsiteDev.bucketArn}/*`,
      ],
      effect: iam.Effect.ALLOW,
      actions: [
        's3:GetObject',
        's3:HeadObject',
        's3:ListBucket',
      ],
    }))
    if (props.isAdmin) {
      lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
        resources: [
          `${bucketDataAdmin.bucketArn}`,
          `${bucketDataAdmin.bucketArn}/*`,
        ],
        effect: iam.Effect.ALLOW,
        actions: [
          's3:GetObject',
          's3:PutObject',
          's3:PutObjectTagging',
          's3:ListBucket',
          's3:DeleteObject',
        ],
      }))
      lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
        resources: [
          `arn:aws:cognito-idp:${props.region}:${props.accountId}:userpool/${props.userPoolIdUser}`,
        ],
        effect: iam.Effect.ALLOW,
        actions: [
          'cognito-idp:AdminCreateUser',
          'cognito-idp:AdminDeleteUser',
          'cognito-idp:AdminEnableUser',
          'cognito-idp:AdminDisableUser',
          'cognito-idp:AdminInitiateAuth',
          'cognito-idp:AdminRespondToAuthChallenge',
          'cognito-idp:AdminUserGlobalSignOut',
          'cognito-idp:AdminAddUserToGroup',
          'cognito-idp:AddCustomAttributes',
          'cognito-idp:CreateGroup',
          'cognito-idp:ListUsersInGroup',
          'cognito-idp:ListUsers',
        ],
      }))
    } else {
      lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
        resources: [
          `${bucketDataAdmin.bucketArn}/regular_holiday/*`,
          `${bucketDataAdmin.bucketArn}/limit_hours/*`,
          `${bucketDataAdmin.bucketArn}/day_of_week_limit_hours/*`,
          `${bucketDataAdmin.bucketArn}/pay_per_hour/*`,
        ],
        effect: iam.Effect.ALLOW,
        actions: [
          's3:GetObject',
          's3:HeadObject',
        ],
      }))
      lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
        resources: [
          `${bucketDataAdmin.bucketArn}`,
        ],
        effect: iam.Effect.ALLOW,
        actions: [
          's3:ListBucket',
        ],
      }))
      lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
        resources: [
          `arn:aws:cognito-idp:${props.region}:${props.accountId}:userpool/${props.userPoolIdUser}`,
        ],
        effect: iam.Effect.ALLOW,
        actions: [
          'cognito-idp:ListUsersInGroup',
          'cognito-idp:ListUsers',
        ],
      }))
    }
    lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
      resources: [
        `arn:aws:cognito-idp:${props.region}:${props.accountId}:userpool/${props.userPoolIdUser}`,
      ],
      effect: iam.Effect.ALLOW,
      actions: [
        'cognito-idp:AdminGetUser',
      ],
    }))
    return lambdaFunction
  }
}
