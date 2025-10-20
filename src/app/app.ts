import { Component, signal, OnInit } from '@angular/core'; 
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common'; 
import { HttpClientModule } from '@angular/common/http'; 

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTabsModule } from '@angular/material/tabs';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu'; 
import { MatCardModule } from '@angular/material/card'; 

import { ApiService } from './api'; 

@Component({
  selector: 'app-root',
  standalone: true, 
  imports: [
    RouterOutlet,
    CommonModule,
    MatToolbarModule,
    MatTabsModule,
    MatIconModule,
    MatButtonModule,
    MatMenuModule,
    MatCardModule,
    HttpClientModule,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  protected readonly title = signal('metalyse-app');

  constructor(private apiService: ApiService) {} 

  ngOnInit(): void {
    this.apiService.checkStatus().subscribe({
      next: (resposta) => {
        console.log('✅ Backend Python (API) está Online! Resposta:', resposta);
      },
      error: (erro) => {
        console.error('❌ ERRO: Não foi possível conectar ao backend Python.', erro);
      }
    });
  }

  goBack() {
    console.log('Ação: Navegar para trás (simulação)');
  }

  reload() {
    console.log('Ação: Recarregar página (simulação)');
  }
}
