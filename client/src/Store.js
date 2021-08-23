import { createStore } from 'vuex'

let userData = undefined
try {
  userData = JSON.parse(localStorage.getItem('userData'))
} catch {}


const Store = createStore({
  state () {
    return {
      user: userData,
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
      
    }
  },
  actions: {
    
    login (context, {username, password}) {
      context.commit('setLoading', true)
      return new Promise(async (resolve, reject) => {
        try { 

          await fetch('http://127.0.0.1:8000/api/login/', {
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
      return new Promise(async (resolve, reject) => {
        try { 

          await fetch('http://127.0.0.1:8000/api/logout/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            }
          }).then(res => {
            console.log(res)
            if(res.status !== 200) {
              throw new Error('Error')
            }
            res.json().then(data => {
              context.commit('setLoading', false)
              context.commit('setUserData', undefined)
              localStorage.setItem('userData', undefined)
              resolve()
            })
          })
        } catch(err) {
          console.log(err)
          context.commit('setLoading', false)
          reject(err)
        }

      })
    }
  }
})

export default Store