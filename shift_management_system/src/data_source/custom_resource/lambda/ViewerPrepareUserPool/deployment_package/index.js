'use strict';
const cfnResponse = require('./cfn-response');
const AWS = require('aws-sdk');

exports.handler = async (event, context, callback) => {
    console.log(JSON.stringify(event));
    if (!(event.RequestType === 'Create')) {
        cfnResponse.send(event, context, cfnResponse.SUCCESS);
        return callback(null, 'SUCCESS');
    }

    try {
        const environment = event.ResourceProperties.NotificationConfiguration.LambdaFunctionConfigurations[0];
        var response;

        var cognitoIdentityServiceProvider = new AWS.CognitoIdentityServiceProvider({apiVersion: '2016-04-18', region: environment.REGION});
        response = await cognitoIdentityServiceProvider.updateUserPool({
            UserPoolId: environment.USER_POOL_ID,
            AdminCreateUserConfig: {
                AllowAdminCreateUserOnly: true
            },
            Policies: {
                PasswordPolicy: {
                    MinimumLength: '6',
                }
            },
        }).promise();
    } catch (err) {
        console.log(err);
        console.log('error !!');
        cfnResponse.send(event, context, cfnResponse.FAILED);
        return callback(null, 'SUCCESS');
    }

    cfnResponse.send(event, context, cfnResponse.SUCCESS);
    return callback(null, 'SUCCESS');
}
