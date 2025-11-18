import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  console.log('🕵️ INTERCEPTOR ACIONADO PARA:', req.url); // <--- ADICIONE ISSO
  
  const token = localStorage.getItem('access_token');
  console.log('🔑 TOKEN NO STORAGE:', token); // <--- ADICIONE ISSO

  if (token) {
    const clonedReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
    return next(clonedReq);
  }
  return next(req);
};