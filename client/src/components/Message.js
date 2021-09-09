import { mapState } from 'vuex'

export default {
    computed: mapState([
        'message', 'loading'
    ]),
    created() {
        
        this.$store.dispatch('fetchMessage', {
            id: this.$route.params.id
        })
        
      },
    template: `
      <div>Message {{ $route.params.id }}</div>
      <div>{{ message }}</div>

      
    `
}

