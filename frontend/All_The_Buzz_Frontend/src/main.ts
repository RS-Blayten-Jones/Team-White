import './assets/styles.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const cors = require('cors')
const app = createApp(App)
app.use(cors());

app.use(router)

app.mount('#app')
