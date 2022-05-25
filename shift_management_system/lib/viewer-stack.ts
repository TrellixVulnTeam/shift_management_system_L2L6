import cdk = require('@aws-cdk/core');
import apiGateway = require('@aws-cdk/aws-apigateway')
import lambda = require("@aws-cdk/aws-lambda")
import s3 = require("@aws-cdk/aws-s3");
import CreateLambdaViewerApi from './CreateLambdaViewerApi'
import CreateRestApi from './CreateRestApi'

export interface ViewerStackProps extends cdk.StackProps {
  readonly isAdmin: boolean
	readonly projectName: string
	readonly bucketDataUser: s3.Bucket
	readonly bucketDataAdmin: s3.Bucket
	readonly bucketViewerWebsite: s3.Bucket
	readonly bucketViewerWebsiteDev: s3.Bucket
	readonly userPoolIdUser: string
	readonly userPoolClientIdUser: string
	readonly userPoolIdAdmin: string
	readonly userPoolClientIdAdmin: string
  readonly region: string
  readonly accountId: string
  readonly version: string
	readonly clientName: string
	readonly distributionDomainName: string
	readonly distributionDomainNameDev: string
}

export class ViewerStack extends cdk.Stack {

  readonly restApi: apiGateway.RestApi
  readonly restApiStaging: apiGateway.RestApi
	readonly lambdaLayerInsertSttDataToRDS: lambda.LayerVersion
	readonly lambdaFunctionForApi: lambda.Function
	readonly lambdaFunctionForApiStaging: lambda.Function

  constructor(scope: cdk.Construct, id: string, props: ViewerStackProps) {
    super(scope, id, props);

		{
			const rtn = this.createApi(props)
			this.restApi = rtn.prod.api
			this.lambdaFunctionForApi = rtn.prod.lambda
			this.restApiStaging = rtn.staging.api
			this.lambdaFunctionForApiStaging = rtn.staging.lambda
		}
  }

	private createApi(props: ViewerStackProps) {
    const lambdaFunctionForApi: lambda.Function = CreateLambdaViewerApi.execute(this,
			false, // admin
			props.bucketDataUser,
			props.bucketDataAdmin,
			props.bucketViewerWebsite,
			props.bucketViewerWebsiteDev,
			props,
		)
    const restApi: apiGateway.RestApi = CreateRestApi.execute(this, false, lambdaFunctionForApi, props)

    const lambdaFunctionForApiStaging: lambda.Function = CreateLambdaViewerApi.execute(this,
			true, // staging
			props.bucketDataUser,
			props.bucketDataAdmin,
			props.bucketViewerWebsite,
			props.bucketViewerWebsiteDev,
			props,
		)
    const restApiStaging: apiGateway.RestApi = CreateRestApi.execute(this, true, lambdaFunctionForApiStaging, props)

		return {
			prod: {
				api: restApi,
				lambda: lambdaFunctionForApi
			},
			staging: {
				api: restApiStaging,
				lambda: lambdaFunctionForApiStaging
			}
		}
	}
}
