import cdk = require('@aws-cdk/core')
import lambda = require("@aws-cdk/aws-lambda")
import iam = require('@aws-cdk/aws-iam')
import cognito = require('@aws-cdk/aws-cognito')
import { DataSourceStackProps } from './data-source-stack'

export default class CreateLambdaPrepareUserPool {
  public static execute(stack: cdk.Stack, userPool: cognito.UserPool, lambdaEnvironment: {}, props: DataSourceStackProps):lambda.Function  {
		const lambdaFunction: lambda.Function = new lambda.Function(stack, `viewer-prepare-user-pool-${props.isAdmin ? "admin" : "user"}`, {
			runtime: lambda.Runtime.NODEJS_12_X,
			code: lambda.Code.fromAsset('src/data_source/custom_resource/lambda/ViewerPrepareUserPool/deployment_package'),
			handler: 'index.handler',
			environment: lambdaEnvironment,
			functionName: `${props.projectName}-prepare-user-pool-${props.isAdmin ? "admin" : "user"}`,
			description: `Cognitoユーザープール${userPool.userPoolProviderName}の追加設定を行う。-${props.isAdmin ? "admin" : "user"}`,
			timeout: cdk.Duration.minutes(3),
		});
    lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
			effect: iam.Effect.ALLOW,
			resources: [
			  userPool.userPoolArn,
			],
			actions: [
        'cognito-idp:UpdateUserPool',
			],
		}))
    return lambdaFunction
  }
}
