const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  pwa: {
    iconPaths: {
        favicon32: 'public/favicon.ico',
    },
    name: "Loyalty",
    themeColor: "#0f476f"
}
})
