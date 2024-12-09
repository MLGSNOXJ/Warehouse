<!-- src/components/LoadingSpinner.vue -->
<template>
    <div class="spinner-overlay" v-if="visible">
      <div class="spinner"></div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoadingSpinner',
    props: {
      visible: {
        type: Boolean,
        default: false
      }
    }
  };
  </script>
  
  <style scoped>
  .spinner-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
  
  .spinner {
    border: 8px solid #f3f3f3;
    border-radius: 50%;
    border-top: 8px solid #3498db;
    width: 60px;
    height: 60px;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>
  