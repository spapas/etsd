import { createStore } from 'vuex'

const Store = createStore({
  state () {
    return {
      user: undefined,
      pkdata: undefined,
      loading: false
    }
  },
  mutations: {
    setLoading (state, status) {
      state.loading = status
    }
  },
  actions: {
    
    login (context, {username, password}) {
      context.commit('setLoading', true)
      return new Promise(async (resolve, reject) => {
        try { 
          let get = await fetch('http://127.0.0.1:8000/users/user-view/', {
            method: 'GET',
            credentials: 'same-origin',
          })
          console.log('ok')

          console.log(get)
          console.log(get.headers)
          window.gt = get

          let koko = await fetch('http://127.0.0.1:8000/users/user-view/', {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrf_token
              
            },
            credentials: 'include',
            body: JSON.stringify({
              username: username,
              password: password
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