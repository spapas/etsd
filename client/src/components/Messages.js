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
    
        <ul>
            <li v-for='message in messages' :key="message.id">
                {{ message }}
            </li>
        </ul>
    `
}

