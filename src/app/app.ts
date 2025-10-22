// ARQUIVO: src/app/app.ts 

import { Component, signal, OnInit } from '@angular/core'; 
import { CommonModule } from '@angular/common'; 
import { HttpClientModule } from '@angular/common/http'; 
import { FormsModule } from '@angular/forms'; 

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTabsModule } from '@angular/material/tabs';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu'; 
import { MatCardModule } from '@angular/material/card'; 

import { ApiService } from './api'; 

import { Login } from './login/login';
import { Cadastro } from './cadastro/cadastro'; 
import { HomeComponent } from './home/home'; 


@Component({
  selector: 'app-root',
  standalone: true, 
  imports: [
    CommonModule,
    HttpClientModule,
    FormsModule, 
    
    Login, 
    Cadastro, 
    HomeComponent, 

    MatToolbarModule,
    MatTabsModule,
    MatIconModule,
    MatButtonModule,
    MatMenuModule,
    MatCardModule,
  ],
  templateUrl: './app.html', 
  styleUrl: './app.css'
})
export class App implements OnInit {
  protected readonly title = signal('metalyse-app');
  
  telaAtual: 'login' | 'cadastro' | 'home' = 'home'; 
  
  constructor(private apiService: ApiService) {} 

  ngOnInit(): void {
    this.apiService.checkStatus().subscribe({
        next: (resposta) => console.log('✅ Backend Python (API) está Online!'),
        error: (erro) => console.error('❌ ERRO: Não foi possível conectar ao backend Python.')
    });
  }

  mudarTela(tela: 'login' | 'cadastro' | 'home') {
    this.telaAtual = tela;
  }
}