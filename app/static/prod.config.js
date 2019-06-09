const path = require('path');

module.exports = {
    entry: "./src/index.js",
    mode: "production",
    output: {
        "path": path.resolve(__dirname, "dist"),
        "filename": "[name].bundle.js"
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
            }
        ]
    }
};
