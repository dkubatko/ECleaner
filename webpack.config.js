var path = require('path');
var webpack = require('webpack');
var glob = require('glob');

module.exports = {
    entry: {
      mounters: glob.sync('./static/mounters/*.jsx'),
    },
    output: {
      path: __dirname + '/static/dist',
      filename: '[name].js'
    },
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
            options: {
              presets: ['@babel/react']
            }
          }
        },
        {
          test: /\.s[ac]ss$/i,
          use: [
            // Creates `style` nodes from JS strings
            'style-loader',
            // Translates CSS into CommonJS
            'css-loader',
            // Compiles Sass to CSS
            'sass-loader',
          ],
        },
      ]
    },
    stats: {
        colors: true
    },
    devtool: 'source-map',
    watch: true,
    
};
