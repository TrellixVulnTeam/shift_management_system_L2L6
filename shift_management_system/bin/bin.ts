#!/usr/bin/env node
import 'source-map-support/register'
import cdk = require('@aws-cdk/core')
import { DataSourceStack } from '../lib/data-source-stack'
import { ViewerStack } from '../lib/viewer-stack'

console.log('tsnode start!!')

const projectName: string = `tlq5muk47x`
const accountId: string = `645485874465`
const region: string = `ap-northeast-1`
const version: string = `20220122-1`
//const version: string = `20210510-1`
const clientName: string = `日本アドカスタム株式会社`

const app = new cdk.App()
let dataSourceStackAdmin = new DataSourceStack(app, `${projectName}-DataSourceStack-Admin`, {
  env: {
    account: accountId,
    region: region,
  },
  projectName: projectName,
  userPoolName: `user-pool`,
  userPoolClientName: `user-pool-client`,
  idPoolName: `id-pool`,
  isAdmin: true,
  accountId: accountId,
  region: region,
  version: version,
  clientName: clientName,
})
let dataSourceStackUser = new DataSourceStack(app, `${projectName}-DataSourceStack-User`, {
  env: {
    account: accountId,
    region: region,
  },
  projectName: projectName,
  userPoolName: `user-pool`,
  userPoolClientName: `user-pool-client`,
  idPoolName: `id-pool`,
  isAdmin: false,
  accountId: accountId,
  region: region,
  version: version,
  clientName: clientName,
})
new ViewerStack(app, `${projectName}-ViewerStack-Admin-${version}`, {
  bucketDataUser: dataSourceStackUser.mainBucket,
  bucketDataAdmin: dataSourceStackAdmin.mainBucket,
  bucketViewerWebsite: dataSourceStackAdmin.bucketViewerWebsite,
  bucketViewerWebsiteDev: dataSourceStackAdmin.bucketViewerWebsiteDev,
  userPoolIdAdmin: dataSourceStackAdmin.userPool.userPoolId,
  userPoolClientIdAdmin: dataSourceStackAdmin.userPoolClient.userPoolClientId,
  userPoolIdUser: dataSourceStackUser.userPool.userPoolId,
  userPoolClientIdUser: dataSourceStackUser.userPoolClient.userPoolClientId,
  env: {
    account: accountId,
    region: region,
  },
  projectName: projectName,
  isAdmin: true,
  accountId: accountId,
  region: region,
  version: version,
  clientName: clientName,
  distributionDomainName: dataSourceStackAdmin.cloudFrontDistribution.distributionDomainName,
  distributionDomainNameDev: dataSourceStackAdmin.cloudFrontDistributionDev.distributionDomainName,
})
new ViewerStack(app, `${projectName}-ViewerStack-User-${version}`, {
  bucketDataUser: dataSourceStackUser.mainBucket,
  bucketDataAdmin: dataSourceStackAdmin.mainBucket,
  bucketViewerWebsite: dataSourceStackUser.bucketViewerWebsite,
  bucketViewerWebsiteDev: dataSourceStackUser.bucketViewerWebsiteDev,
  userPoolIdAdmin: dataSourceStackAdmin.userPool.userPoolId,
  userPoolClientIdAdmin: dataSourceStackAdmin.userPoolClient.userPoolClientId,
  userPoolIdUser: dataSourceStackUser.userPool.userPoolId,
  userPoolClientIdUser: dataSourceStackUser.userPoolClient.userPoolClientId,
  env: {
    account: accountId,
    region: region,
  },
  projectName: projectName,
  isAdmin: false,
  accountId: accountId,
  region: region,
  version: version,
  clientName: clientName,
  distributionDomainName: dataSourceStackUser.cloudFrontDistribution.distributionDomainName,
  distributionDomainNameDev: dataSourceStackUser.cloudFrontDistributionDev.distributionDomainName,
})
console.log('tsnode finish!!')
