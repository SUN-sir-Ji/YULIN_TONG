<template>
  <div>
    <IndexPage v-if="currentPage === 'index'"
      @goToLogin="goToLogin"
      @goToRegister="goToRegister"
    />
    
    <LoginPage v-else-if="currentPage === 'login'"
      @goToFindPassword="goToFindPassword"
      @goToHomepage="goToHomepage"
      @goToRegister="goToRegister"
      @goToIndex="goToIndex"
    />
    <RegisterPage v-else-if="currentPage === 'register'"
     @goToIndex="goToIndex"
     @goToLogin="goToLogin"
     @Registersuccess="Registersuccess"
    />
    <FindPasswordPage v-else-if="currentPage === 'findPassword'"
      @goToLogin="goToLogin"
      @goToRegister="goToRegister"
    />
    <HomepagePage v-else-if="currentPage === 'homepage'"
    @goToLogin="goToLogin"
    @goToPlantHome="goToPlantHome"
    @goToAbout="goToAbout"
     @goToIdentify="goToIdentify"
     />
     <PlantHome v-else-if="currentPage === 'planthome'"
     @goToHomepage1="goToHomepage1"
     @goToPlantimage="goToPlantimage"
     />

    <plantimage v-else-if="currentPage === 'plantimage'"
     @goToPlantHome=" goToPlantHome"/>

    <Loading v-if="isLoading" />
    
    <!-- 删除了Password组件引用 -->
    
    <About v-else-if="currentPage === 'about'"
     @goToHomepage1="goToHomepage1"/>
     
     <Identify v-else-if="currentPage ==='identify'"
     @goToHomepage1="goToHomepage1"
    />
     
    <registersuccess v-if="isRegister"
    @Registersuccess="Registersuccess"
    @goToLogin="goToLogin"/>
    </div>
  </template>

  <script>
  
  import IndexPage from './pages/index/index.vue';
  import LoginPage from './pages/login/login.vue';
  import RegisterPage from './pages/login/register.vue';
  import FindPasswordPage from './pages/login/findPassword.vue';
  import HomepagePage from './pages/Home/homepage.vue';
  import Loading from './components/Loading.vue';
  import registersuccess from './components/registersuccess.vue';
  import PlantHome from './pages/plant/plantHome.vue';
  import Plantimage from './pages/plant/plantimage.vue';
  import About from './pages/about/about.vue';
  import Identify from './pages/identify/identify.vue';
  
  export default {
    components: {
      IndexPage,
      LoginPage,
      RegisterPage,
      FindPasswordPage,
      HomepagePage,
      Loading,
      registersuccess,
      PlantHome,
      Plantimage,
      About,
      Identify
    },
    data() {
      return {
        currentPage: 'index',
        isLoading: false,
        // 删除了isPassword状态变量
        isRegister: false
      };
    },
    mounted() {
      
    },
    methods: {
      goToIndex() {
        this.currentPage = 'index';
      },
      goToLogin() {
    
          this.currentPage = 'login';
       
      },
      goToRegister() {
        this.currentPage = 'register';
      },
      goToFindPassword() {
        this.currentPage = 'findPassword';
      },
      goToHomepage() {
        this.isLoading = true;
        setTimeout(() => {
          this.currentPage = 'homepage';
          this.isLoading = false;
        }, 1000); 
      },
      goToHomepage1() {
          this.currentPage = 'homepage';
      }
    ,Registersuccess() {
      this.isRegister =  !this.isRegister;
  },
   goToPlantHome() {
    this.currentPage = 'planthome';
    },
    goToPlantimage() {
    this.currentPage = 'plantimage';
    },
    goToAbout() {
    this.currentPage = 'about';
    },
    goToIdentify() {
    this.currentPage = 'identify';
    },
  }
  }
  </script>
  
  <style >
    
  
  </style>
  
  