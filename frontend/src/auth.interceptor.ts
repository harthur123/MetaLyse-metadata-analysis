// src/app/auth.interceptor.ts
import { HttpInterceptorFn, HttpRequest, HttpHandlerFn } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req: HttpRequest<unknown>, next: HttpHandlerFn) => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token');

  // Não mexa no Content-Type se for multipart/form-data (FormData) — apenas clone e adicione Authorization
  const headers = token ? req.headers.set('Authorization', `Bearer ${token}`) : req.headers;
  const authReq = req.clone({ headers });

  return next(authReq);
};
