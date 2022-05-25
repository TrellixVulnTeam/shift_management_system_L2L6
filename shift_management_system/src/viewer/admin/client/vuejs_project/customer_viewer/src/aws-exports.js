import Amplify from 'aws-amplify'
Amplify.configure({
  Auth: {
    // フェデレーションアイデンティティのID
    identityPoolId: process.env.VUE_APP_COGNITO_IDENTITY_POOL_ID,
    // リージョン
    region: process.env.VUE_APP_COGNITO_REGION,
    // ユーザープールのID
    userPoolId: process.env.VUE_APP_COGNITO_USER_POOL_ID,
    // ユーザープールのウェブクライアントID
    userPoolWebClientId: process.env.VUE_APP_COGNITO_CLIENT_ID,
    mandatorySignIn: true
  },
  API: {
    endpoints: [
      {
        name: process.env.VUE_APP_API_NAME,
        endpoint: process.env.VUE_APP_API_ENDPOINT,
        region: process.env.VUE_APP_API_REGION
      },
      {
        name: process.env.VUE_APP_API_NAME_STAGING,
        endpoint: process.env.VUE_APP_API_ENDPOINT_STAGING,
        region: process.env.VUE_APP_API_REGION
      },
      {
        name: process.env.VUE_APP_API_ADDRESS_MASTER_NAME,
        endpoint: process.env.VUE_APP_API_ADDRESS_MASTER_ENDPOINT,
        region: process.env.VUE_APP_API_REGION
      }
    ]
  }
})
