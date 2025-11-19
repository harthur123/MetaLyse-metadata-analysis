// ARQUIVO: src/app/api.ts

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_URL = 'http://localhost:5000/api'; 

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  // GET genérico
  get(endpoint: string, headers?: HttpHeaders): Observable<any> {
    return this.http.get(`${API_URL}${endpoint}`, { headers });
  }

  // POST genérico
  post(endpoint: string, body: any, headers?: HttpHeaders): Observable<any> {
    return this.http.post(`${API_URL}${endpoint}`, body, { headers });
  }

  // GET específico
  getRelatorios(): Observable<any> {
    return this.http.get(`${API_URL}/relatorios`);
  }

  // POST específico para análise de arquivo
  analisarArquivo(dadosArquivo: FormData): Observable<any> {
    return this.http.post(`${API_URL}/analisar`, dadosArquivo);
  }

  // Status do backend
  checkStatus(): Observable<any> {
    return this.http.get(`${API_URL}/status`);
  }
}
