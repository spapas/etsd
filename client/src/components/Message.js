import { mapState } from 'vuex'

export default {
    computed: mapState([
        'messages', 'loading'
    ]),
    created() {
        
        if(this.messages== undefined) {
            this.$store.dispatch('fetchMessages')
        }

      },
    template: `
      <div>Message {{ $route.params.id }}</div>
    `
}

