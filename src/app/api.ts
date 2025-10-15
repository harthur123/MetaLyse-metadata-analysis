// ARQUIVO: src/app/api.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'; // <-- 1. Importar HttpClient
import { Observable } from 'rxjs';


const API_URL = 'http://localhost:5000/api'; 

@Injectable({
  
  providedIn: 'root'
})
export class ApiService {
  
  constructor(private http: HttpClient) { }

 
  getRelatorios(): Observable<any> {
    return this.http.get(`${API_URL}/relatorios`);
  }

  
  analisarArquivo(dadosArquivo: FormData): Observable<any> {
    
    return this.http.post(`${API_URL}/analisar`, dadosArquivo);
  }

 
  checkStatus(): Observable<any> {
    return this.http.get(`${API_URL}/status`);
  }
}
