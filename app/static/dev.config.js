const path = require('path');

module.exports = {
    entry: "./src/index.js",
    output: {
        "path": path.resolve(__dirname, "dist"),
        "filename": "[name].bundle.js"
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                // use: {
                //     loader: "babel-loader",
                //     options: {
                //         presets: [
                //             "@babel/env",
                //             "@babel/react"
                //         ]
                //     }
                // }
            }
        ]
    }
};
