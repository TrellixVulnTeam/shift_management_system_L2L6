import cdk = require('@aws-cdk/core');
import lambda = require("@aws-cdk/aws-lambda");
import apiGateway = require('@aws-cdk/aws-apigateway');
import cognito = require('@aws-cdk/aws-cognito')
import { ViewerStackProps } from './viewer-stack'

export default class CreateRestApi {
  public static execute(
    stack: cdk.Stack,
    isStaging: boolean,
    lambdaFunction: lambda.Function,
    props: ViewerStackProps,
  ):apiGateway.RestApi  {

    var apiName = 'ViewerAPIGateway'
    var description = `ビューアー用APIGateway [(${props.projectName})]${props.version}`
    var authorizerName = 'AICallViewerAPIAuthorizer'
    if (isStaging) {
        apiName += '_staging'
        description += '_staging'
        authorizerName += '_staging'
    }

    const api: apiGateway.RestApi = new apiGateway.RestApi(stack, apiName, {
      restApiName: `${apiName}-${props.isAdmin ? "admin" : "user"}-${props.version}`,
      description: description,
      deploy: true,
      binaryMediaTypes: ['*/*'],
      minimumCompressionSize: 0,
      deployOptions: {
        stageName: props.version,
        description: `[${props.version})]`,
        dataTraceEnabled: true,
        loggingLevel: apiGateway.MethodLoggingLevel.INFO,
      },
    });
    const cognitoAuthorizer: apiGateway.CfnAuthorizer = new apiGateway.CfnAuthorizer(
      stack,
      authorizerName,
      {
        restApiId: api.restApiId,
        identitySource: "method.request.header.Authorization",
        providerArns: [
          `arn:aws:cognito-idp:${props.region}:${props.accountId}:userpool/${props.isAdmin ? props.userPoolIdAdmin : props.userPoolIdUser}`,
        ],
        name: "CognitoAuthorizer",
        type: 'COGNITO_USER_POOLS'
      }
    )
    const proxy: apiGateway.Resource = api.root.addResource('{proxy+}', {
      defaultIntegration: new apiGateway.LambdaIntegration(lambdaFunction),
    })
    proxy.addMethod('ANY', new apiGateway.LambdaIntegration(lambdaFunction), {
      authorizationType: apiGateway.AuthorizationType.COGNITO,
      authorizer: {
        authorizerId: cognitoAuthorizer.ref,
      },
    })
    proxy.addMethod('OPTIONS', new apiGateway.LambdaIntegration(lambdaFunction))

    const appHash: apiGateway.Resource = api.root.addResource('app_hash', {
      defaultIntegration: new apiGateway.LambdaIntegration(lambdaFunction),
    })
    appHash.addMethod('OPTIONS', new apiGateway.LambdaIntegration(lambdaFunction), {})
    appHash.addMethod('GET', new apiGateway.LambdaIntegration(lambdaFunction), {})

    const test: apiGateway.Resource = api.root.addResource('test', {
      defaultIntegration: new apiGateway.LambdaIntegration(lambdaFunction),
    })
    test.addMethod('OPTIONS', new apiGateway.LambdaIntegration(lambdaFunction), {})
    test.addMethod('GET', new apiGateway.LambdaIntegration(lambdaFunction), {})
    return api
  }
}
