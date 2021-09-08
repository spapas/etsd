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
    
        <table class='table'>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Protocol</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for='message in messages' :key="message.mesage_id">
                    <td><router-link class="btn btn-sm btn-primary" :to="'/message/' + message.message_id ">{{ message.message_id }}</router-link></td>
                    <td>
                        <span v-if="message.message.protocol">
                            {{ message.message.protocol }} / {{ message.message.protocol_year }}
                        </span>
                        <span v-else>
                            Draft message
                        </span>
                    </td>
                    <td>{{ message }}</td>
                </tr>
            </tbody>
        </table>
    `
}

