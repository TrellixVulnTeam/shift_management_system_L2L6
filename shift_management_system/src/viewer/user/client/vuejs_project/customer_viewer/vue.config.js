/*
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
var path = require('path')
var webpack = require('webpack')
*/
function uuidv4() { // Public Domain/MIT
    var d = new Date().getTime();//Timestamp
    var d2 = ((typeof performance !== 'undefined') && performance.now && (performance.now()*1000)) || 0;//Time in microseconds since page-load or 0 if unsupported
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16;//random number between 0 and 16
        if(d > 0){//Use timestamp until depleted
            r = (d + r)%16 | 0;
            d = Math.floor(d/16);
        } else {//Use microseconds since page-load if supported
            r = (d2 + r)%16 | 0;
            d2 = Math.floor(d2/16);
        }
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
}

module.exports = {
  publicPath: process.env.NODE_ENV.endsWith('-prod')
    ? `${process.env.BASE_URL}`
    : `./`,
  runtimeCompiler: true,
  lintOnSave: true,
  productionSourceMap: false,
  parallel: true,
  configureWebpack: (config) => {
    config.devServer = {
      watchOptions: {
        poll: 3000
      },
      compress: false,
      overlay: {
        warnings: true,
        errors: true
      }
    }

    config.optimization = {
      usedExports: true,
      minimize: true,
      splitChunks: {
        minSize: 100000,
        maxSize: 2000000,
        chunks: 'async',
        /*
        minSize: 30000,
        maxSize: 0,
        */
        minChunks: 1,
        maxAsyncRequests: 5,
        maxInitialRequests: 3,
        automaticNameDelimiter: '~',
        name: true,
        cacheGroups: {
          commons: {
            //test: /[\\/]node_modules[\\/]/,
            // cacheGroupKey here is `commons` as the key of the cacheGroup
            name(module, chunks, cacheGroupKey) {
              const moduleFileName = module
                .identifier()
                .split('/')
                .reduceRight((item) => item);
              const allChunksNames = chunks.map((item) => item.name).join('~');

              console.log(`${cacheGroupKey}-${allChunksNames}-${uuidv4()}-${moduleFileName}`);
              return `${cacheGroupKey}-${allChunksNames}-${uuidv4()}-${moduleFileName}`;
            },
            chunks: 'all',
          },
          vendors: {
            test: /[\\/]node_modules[\\/]/,
            // cacheGroupKey here is `commons` as the key of the cacheGroup
            name(module, chunks, cacheGroupKey) {
              const moduleFileName = module
                .identifier()
                .split('/')
                .reduceRight((item) => item);
              const allChunksNames = chunks.map((item) => item.name).join('~');

              console.log(`${cacheGroupKey}-${allChunksNames}-${uuidv4()}-${moduleFileName}`);
              return `${cacheGroupKey}-${allChunksNames}-${uuidv4()}-${moduleFileName}`;
            },
            chunks: 'all',
          },
          /*
          vendors: {
            test: /[\\/]node_modules[\\/]/,
            // cacheGroupKey here is `commons` as the key of the cacheGroup
            name(module, chunks, cacheGroupKey) {
              const moduleFileName = module
                .identifier()
                .split('/')
                .reduceRight((item) => item);
              const allChunksNames = chunks.map((item) => item.name).join('~');

              console.log(`${cacheGroupKey}-${allChunksNames}-${uuidv4()}-${moduleFileName}`);
              return `${cacheGroupKey}-${allChunksNames}-${uuidv4()}-${moduleFileName}`;
            },
            chunks: 'initial',
          },
          */
          /*
          vendors: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: -10,
            chunks: 'initial'
          },
          common: {
            name: 'chunk-common',
            minChunks: 2,
            priority: -20,
            chunks: 'initial',
            reuseExistingChunk: true
          },
          */
          /*
          vendors: {
            test: /[\\/]node_modules[\\/]/, // this is what you are looking for
            priority: -10
          },
          default: {
            minChunks: 2,
            priority: -20,
            reuseExistingChunk: true
          },
          */
        },
      }
    }

    /*
    config.module = {
      rules: [
        {
          test: /\.js$/,
          loader: 'babel-loader',
          exclude: /node_modules/,
        }
      ]
    }
    */
  },
  chainWebpack: config => {
    config.module.rules.delete('scss')
    let scssRule = config.module.rule('scss')
      .exclude
        .add(/node_modules/)
        .end();
    scssRule
      .test(/\.scss$/);
    [
      { name: 'vue-style-loader' },
      { name: 'fast-css-loader' },
      { name: 'fast-sass-loader' }
    ].forEach((load) => {
      scssRule
        .use(load.name)
        .loader(load.loader || load.name)
        .options(load.options || {})
    })
    // disable cache for prod only, remove the if to disable it everywhere
    if (process.env.NODE_ENV.endsWith('-prod')) {
      config.module.rule('vue').uses.delete('cache-loader');
      config.module.rule('js').uses.delete('cache-loader');
      config.module.rule('ts').uses.delete('cache-loader');
      config.module.rule('tsx').uses.delete('cache-loader');
    }
  },
  css: {
    loaderOptions: {
      sass: {
        data: `@import "@/assets/scss/global.scss";`
      }
    }
  },
  productionSourceMap: false,
}