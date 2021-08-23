const Nav = {
    props: ['user', 'pkdata'],
    template: `
<nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">E · T · S · D</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarMain" aria-controls="navbarMain"
        aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
  
      <div class="collapse navbar-collapse" id="navbarMain">
        <div class='container-fluid d-flex justify-content-between'>
          <ul class="navbar-nav mr-auto mb-2 mb-md-0" v-if='user'>
            
            <li class="nav-item" v-if='user'>
                <router-link class="nav-link" to="/messages">Messages</router-link>
            </li>
            <li class="nav-item" v-if='user'>
                <router-link class="nav-link" to="/privatekey_load"><span class='text-danger'>Load private key</span></router-link>
            </li>
            <li class="nav-item" v-if='user'>
                <router-link class="nav-link" to="/public_key_list"><span class='text-info'>Public key List</span></router-link>
            </li>

            
            <li class="nav-item">
                <router-link class="nav-link" to="/help"><span class='text-warning'>Help</span></router-link>
              
            </li>
          </ul>
          
          <ul class="navbar-nav ">
            <li class="nav-item" v-if='user'>
              
                <a v-if='pkdata' class="btn btn-outline-danger btn-sm"
                    data-bs-toggle="tooltip" 
                    data-bs-html="true" 
                    data-bs-placement="bottom" 
                    title="Fingerprint: <b>{{ pkdata.fingerprint }}</b><br/>User id: <b>{{ pkdata.user_id|escape }}</b>"
                    href='{{ request.path }}'
                    >
                    <b>{% trans "Private key loaded" %} <span id='countdowntimer'>15:00</span></b>
                </a>
                
                <router-link class="btn btn-outline-info btn-sm" to="/logout">
                  ({{ user }}) | Disconnect
                </router-link>
            </li>
            <li class="nav-item" v-if='!user'>
                <router-link class="btn btn-outline-info btn-sm" to="/login">
                    Please login
                </router-link>
            </li>
          </ul>
        </div> <!-- container-fluid-->
      </div> <!-- navbarMain -->
    </div> <!-- container -->
  </nav>        
`
}

export default Nav