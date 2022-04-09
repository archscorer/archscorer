module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  outputDir: 'django/frontend',
  assetsDir: 'static',
  devServer: {
    public: 'localhost',
    proxy: {
      '^/api': {
        target: 'http://localhost:8008',
        ws: true,
        changeOrigin: true
      },
      '^/accounts': {
        target: 'http://localhost:8008',
        ws: true,
        changeOrigin: true
      },
      '^/static': {
        target: 'http://localhost:8008',
        ws: true,
        changeOrigin: true
      }
    }
  }
}
