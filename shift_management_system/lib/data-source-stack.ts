import cdk = require('@aws-cdk/core');
import ec2 = require("@aws-cdk/aws-ec2");
import s3 = require("@aws-cdk/aws-s3");
import sns = require("@aws-cdk/aws-sns");
import iam = require('@aws-cdk/aws-iam')
import lambda = require('@aws-cdk/aws-lambda')
import events = require('@aws-cdk/aws-events');
import cognito = require('@aws-cdk/aws-cognito')
import cloudfront = require('@aws-cdk/aws-cloudfront')
import CreateBucketViewerWebsite from './CreateBucketViewerWebsite'
import CreateLambdaPrepareUserPool from './CreateLambdaPrepareUserPool'

export interface DataSourceStackProps extends cdk.StackProps {
	readonly isAdmin: boolean
	readonly projectName: string
	readonly userPoolName: string
	readonly userPoolClientName: string
	readonly idPoolName: string
	readonly region: string
	readonly accountId: string
	readonly version: string
	readonly clientName: string
}

export class DataSourceStack extends cdk.Stack {

	readonly mainBucket: s3.Bucket
	readonly userPool: cognito.UserPool
	readonly idPool: cognito.CfnIdentityPool
	readonly userPoolClient: cognito.UserPoolClient

	readonly cloudFrontDistribution: cloudfront.CloudFrontWebDistribution
	readonly bucketViewerWebsite: s3.Bucket
	readonly cloudFrontDistributionDev: cloudfront.CloudFrontWebDistribution
	readonly bucketViewerWebsiteDev: s3.Bucket

	constructor(scope: cdk.Construct, id: string, props: DataSourceStackProps) {
		super(scope, id, props);

		this.mainBucket = new s3.Bucket(this, `bucket-${props.isAdmin ? "admin" : "user"}`, {
			blockPublicAccess: new s3.BlockPublicAccess({
				blockPublicAcls: true,
				blockPublicPolicy: true,
				ignorePublicAcls: true,
				restrictPublicBuckets: true
			}),
			bucketName: `${props.projectName}-bucket-${props.isAdmin ? "admin" : "user"}`,
			removalPolicy: cdk.RemovalPolicy.DESTROY, // cdk destroy時にバケットを消す
			encryption: s3.BucketEncryption.S3_MANAGED // 暗号化
		});

		this.userPool = this.createCognitoUserPool(props)
		this.userPoolClient = this.createUserPoolClient(this.userPool, props)
		this.idPool = this.createIdentityPool(this.userPool, this.userPoolClient, props)
		this.prepareUserPool(this.userPool, props)

		const rtn = this.createViwerWebsite(false, props)
		const rtnDev = this.createViwerWebsite(true, props)
		this.cloudFrontDistribution = rtn.distribution
		this.bucketViewerWebsite = rtn.bucket
		this.cloudFrontDistributionDev = rtnDev.distribution
		this.bucketViewerWebsiteDev = rtnDev.bucket

		new cdk.CfnOutput(this, 'Cognito User Pool Id', {value: `${this.userPool.userPoolId}`})
		new cdk.CfnOutput(this, 'Cognito User Pool ARN', {value: `${this.userPool.userPoolArn}`})
		new cdk.CfnOutput(this, 'Cognito User Pool Client Id', {value: `${this.userPoolClient.userPoolClientId}`})
		new cdk.CfnOutput(this, 'Cognito Id Pool Id', {value: `${this.idPool.ref}`})
		new cdk.CfnOutput(this, 'Viewer Website URL', {value: `https://${this.cloudFrontDistribution.domainName}/`})
		new cdk.CfnOutput(this, 'Viewer Website S3 Bucket', {value: `${this.bucketViewerWebsite.bucketArn}`})
		new cdk.CfnOutput(this, 'Viewer Website URL DEV', {value: `https://${this.cloudFrontDistributionDev.domainName}/`})
		new cdk.CfnOutput(this, 'Viewer Website S3 Bucket DEV', {value: `${this.bucketViewerWebsiteDev.bucketArn}`})
  	}

	private createCognitoUserPool(props: DataSourceStackProps): cognito.UserPool {
		const userPool: cognito.UserPool = new cognito.UserPool(this, 'user-pool-${props.isAdmin ? "admin" : "user"}', {
			userPoolName: `${props.projectName}-${props.userPoolName}-${props.isAdmin ? "admin" : "user"}`,
			signInAliases: {
				username: true,
				email: false,
				phone: false,
				preferredUsername: true,
			},
			selfSignUpEnabled: false,
			autoVerify: {}, // 必須属性なし
		})
		return userPool
	}

	private createUserPoolClient(userPool: cognito.UserPool, props: DataSourceStackProps): cognito.UserPoolClient {
		const userPoolClient: cognito.UserPoolClient = new cognito.UserPoolClient(this, `user-pool-client-${props.isAdmin ? "admin" : "user"}`, {
			userPoolClientName: `${props.projectName}-${props.userPoolClientName}-${props.isAdmin ? "admin" : "user"}`,
		        userPool: userPool,
			authFlows: {
				adminUserPassword: true,
				userSrp: true,
			},
			disableOAuth: true,
	    	})
		return userPoolClient
	}

	private createIdentityPool(userPool: cognito.UserPool, userPoolClient: cognito.UserPoolClient, props: DataSourceStackProps): cognito.CfnIdentityPool {
		const identityPoolName = `${props.projectName}-${props.idPoolName}-${props.isAdmin ? "admin" : "user"}`
    		const identityPool: cognito.CfnIdentityPool = new cognito.CfnIdentityPool(this, `id-pool-${props.isAdmin ? "admin" : "user"}`, {
		      	identityPoolName: identityPoolName,
      			allowUnauthenticatedIdentities: false,
		      	cognitoIdentityProviders: [
				{
					clientId: userPoolClient.userPoolClientId,
					providerName: `cognito-idp.${props.env?.region}.amazonaws.com/${userPool.userPoolId}`,
					serverSideTokenCheck: true,
				}
	      		],
		})
		this.createIdPoolRoleAttachment(identityPool, props)
		return identityPool
	}

	private createIdPoolRoleAttachment(identityPool: cognito.CfnIdentityPool, props: DataSourceStackProps) {
		const _this: cdk.Stack = this
		const createAuthRole = function(): iam.Role {
		const roleName = `${props.projectName}-Cognito_Auth_Role-${props.isAdmin ? "admin" : "user"}`
		const role: iam.Role = new iam.Role(_this, `Cognito_Auth_Role-${props.isAdmin ? "admin" : "user"}`, {
			assumedBy: new iam.FederatedPrincipal(		
				  'cognito-identity.amazonaws.com',
				  {
				    "StringEquals": {
					"cognito-identity.amazonaws.com:aud": identityPool.ref
				    },
				    "ForAnyValue:StringLike": {
					"cognito-identity.amazonaws.com:amr": "authenticated"
				    }
				  },
		  		'sts:AssumeRoleWithWebIdentity'), // この役割を引き受けることができるIAMプリンシパル
			roleName: roleName,
			path: '/',
		})
		role.attachInlinePolicy(new iam.Policy(_this, `${roleName}-inlinePolicy1-${props.isAdmin ? "admin" : "user"}`, {
			policyName: `${roleName}-inlinePolicy1-${props.isAdmin ? "admin" : "user"}`,
			statements: [
			  new iam.PolicyStatement({
			    resources: [ '*' ],
			    actions: [
			      "mobileanalytics:PutEvents",
			      "cognito-identity:*",
			      "cognito-sync:*",
			    ],
			  }),
			],
		}));
		return role;
    }

    const createUnauthRole = function(): iam.Role {
	      const roleName = `${props.projectName}-Cognito_Unauth_Role-${props.isAdmin ? "admin" : "user"}`
	      const role: iam.Role = new iam.Role(_this, `Cognito_Unauth_Role-${props.isAdmin ? "admin" : "user"}`, {
		assumedBy: new iam.FederatedPrincipal(
		  'cognito-identity.amazonaws.com',
		  {
		    "StringEquals": {
			"cognito-identity.amazonaws.com:aud": identityPool.ref
		    },
		    "ForAnyValue:StringLike": {
			"cognito-identity.amazonaws.com:amr": "unauthenticated"
		    }
		  },
		  'sts:AssumeRoleWithWebIdentity'), // この役割を引き受けることができるIAMプリンシパル
		roleName: roleName,
		path: '/',
	      })
	      role.attachInlinePolicy(new iam.Policy(_this, `${roleName}-inlinePolicy1-${props.isAdmin ? "admin" : "user"}`, {
		policyName: `${roleName}-inlinePolicy1-${props.isAdmin ? "admin" : "user"}`,
		statements: [
		  new iam.PolicyStatement({
		    resources: [ '*' ],
		    actions: [
		      "mobileanalytics:PutEvents",
		      "cognito-sync:*"
		    ],
		  }),
		],
	      }));
	      return role;
	    }

	    return new cognito.CfnIdentityPoolRoleAttachment(this, `viewer-id-pool-attachment-${props.isAdmin ? "admin" : "user"}`, {
		identityPoolId: identityPool.ref,
		roles: {
			"authenticated": createAuthRole().roleArn,
			"unauthenticated": createUnauthRole().roleArn,
		}
	    })
	}

	private prepareUserPool(userPool: cognito.UserPool, props: DataSourceStackProps): void {
		const lambdaEnvironment = {
			REGION: props.env?.region,
			USER_POOL_NAME: `${props.projectName}-${props.userPoolName}`,
			USER_POOL_CLIENT_NAME: `${props.projectName}-${props.userPoolClientName}`,
			ID_POOL_NAME: `${props.projectName}-${props.idPoolName}`,
			USER_POOL_ID: userPool.userPoolId,
			USER_POOL_CLIENT_ID: this.userPoolClient.userPoolClientId,
			IDENTITY_POOL_ID: this.idPool.ref,
			IS_ADMIN: props.isAdmin ? `true` : `false`,
		}

		const customResource: cdk.CfnResource = new cdk.CfnResource(this, `custom-resource-prepare-user-pool-${props.isAdmin ? "admin" : "user"}`, {
			type: `Custom::CustomResourcePrepareUserPool-${props.isAdmin ? "admin" : "user"}`,
			properties: {
				ServiceToken: CreateLambdaPrepareUserPool.execute(this, userPool, lambdaEnvironment, props).functionArn,
				NotificationConfiguration: {
					LambdaFunctionConfigurations: [ lambdaEnvironment ]
				},
			},
		});
	}

	private createViwerWebsite(isDev: boolean, props: DataSourceStackProps) {
		const bucketViewerWebsite: s3.Bucket = CreateBucketViewerWebsite.execute(this, isDev, props)
		const identity: cloudfront.OriginAccessIdentity = new cloudfront.OriginAccessIdentity(
			this, `viewer-identity-${props.isAdmin ? "admin" : "user"}${isDev ? "-dev" : ""}`,
			{
			      comment: `${props.isAdmin ? "admin" : "user"}${isDev ? "-dev" : ""}`,
			}
		)

	    	const distribution: cloudfront.CloudFrontWebDistribution = new cloudfront.CloudFrontWebDistribution(
			this,
			`viewer-distribution-${props.isAdmin ? "admin" : "user"}${isDev ? "-dev" : ""}`,
			{
	      			originConfigs: [
			{
			    s3OriginSource: {
			      s3BucketSource: bucketViewerWebsite,
			      originAccessIdentity: identity,
			    },
			    behaviors : [
			      {
				isDefaultBehavior: true,
				defaultTtl: cdk.Duration.seconds(5),
			      }
			    ],
			}
		      ],
		      errorConfigurations: [
			{
			  errorCode: 403,
			  responseCode: 200,
			  responsePagePath: '/',
			},
		        {
			  errorCode: 404,
			  responseCode: 200,
			  responsePagePath: '/',
			}
		      ],
		      comment: `${props.isAdmin ? "admin" : "user"}${isDev ? "-dev" : ""}`,
		});

		bucketViewerWebsite.addToResourcePolicy(new iam.PolicyStatement({
			principals: [new iam.CanonicalUserPrincipal(identity.cloudFrontOriginAccessIdentityS3CanonicalUserId)],
			resources: [`${bucketViewerWebsite.bucketArn}/*`],
			effect: iam.Effect.ALLOW,
			actions: [
				's3:GetObject',
			],
		}))

		return { distribution: distribution, bucket: bucketViewerWebsite }
	}
}
