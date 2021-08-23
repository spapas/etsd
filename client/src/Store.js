import { createStore } from 'vuex'

let userData = undefined
try {
  userData = JSON.parse(localStorage.getItem('userData'))
} catch {}

server = localStorage.getItem('server')
console.log("SERVER IS " , server)

const Store = createStore({
  state () {
    return {
      server,
      user: userData,
      messages: undefined,
      pkdata: undefined,
      loading: false
    }
  },
  mutations: {
    setLoading (state, status) {
      state.loading = status
    },
    setUserData (state, data) {
      state.user = data
    },
    setMessages(state, data) {
      state.messages = data 
    },
    setServer(state, data) {
      state.server = data 
    }
  },
  actions: {
    login (context, {server, username, password}) {
      console.log("LIGIN ", server, context.state)
      context.commit('setLoading', true)
      context.commit('setServer', server)
      localStorage.setItem('server', server)

      return new Promise(async (resolve, reject) => {
        try { 
          
          await fetch(server + '/api/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username: username,
              password: password
            })
          }).then(res => {
            console.log(res)
            if(res.status !== 200) {
              throw new Error('Error')
            }
            res.json().then(data => {
              context.commit('setLoading', false)
              context.commit('setUserData', data)
              localStorage.setItem('userData', JSON.stringify(data))
              
              resolve()
            })
          })
        } catch(err) {
          console.log(err)
          context.commit('setLoading', false)
          reject(err)
        }

      })
    },
    logout (context) {
      context.commit('setLoading', true)
      console.log("LOGOUT ", context.state)
      return new Promise(async (resolve, reject) => {
        try { 

          await fetch(context.state.server + '/api/logout/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Token ${context.state.user.token}`
            }
          }).then(res => {
            console.log(res)
            if(res.status !== 200) {
              throw new Error('Error')
            }
            res.json().then(data => {
              localStorage.setItem('userData', undefined)
              context.commit('setLoading', false)
              context.commit('setUserData', undefined)
              context.commit('setMessages', undefined)
              resolve()
            })
          })
        } catch(err) {
          console.log(err)
          context.commit('setLoading', false)
          reject(err)
        }

      })
    },
    fetchMessages (context) {
      console.log("MESSAGEs ", context.state)
      context.commit('setLoading', true)
      console.log("Fetch messages")
      return new Promise(async (resolve, reject) => {
        await fetch(context.state.server + '/messages/api/messages/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${context.state.user.token}`
          }}).then(res => {
            console.log(res)
            if(res.status !== 200) {
              throw new Error('Error')
            }
            res.json().then(data => {
              context.commit('setLoading', false)
              context.commit('setMessages', data)
            })
          })

      })
    }
  }
})

export default Store