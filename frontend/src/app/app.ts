// ARQUIVO: src/app/app.ts

import { Component, OnInit, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, NavigationEnd, RouterModule } from '@angular/router';
import { filter } from 'rxjs/operators';
import { HttpHeaders } from '@angular/common/http';

// Angular Material
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTabsModule, MatTabNavPanel } from '@angular/material/tabs';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';

import { ApiService } from './api';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    MatToolbarModule,
    MatTabsModule,
    MatIconModule,
    MatButtonModule,
    MatMenuModule,
    RouterModule
  ],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App implements OnInit {

  private router = inject(Router);
  private apiService = inject(ApiService);

  protected readonly title = signal('metalyse-app');
  protected readonly mostrarMenu = signal(true);
  private rotasEscondidas = ['/login', '/cadastro', '/definir-senha', '/reset-password-request'];
  tabPanel: MatTabNavPanel | undefined;

  constructor() {
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe((event: any) => {
        const urlAtual = event.urlAfterRedirects || event.url;
        const deveEsconder = this.rotasEscondidas.some(rota => urlAtual.includes(rota));
        this.mostrarMenu.set(!deveEsconder);
      });
  }

  ngOnInit(): void {
    // Verifica backend
    this.apiService.checkStatus().subscribe({
      next: () => console.log('✅ Backend Python está Online'),
      error: () => console.error('❌ Não foi possível conectar ao backend')
    });
  }

  // ============================
  // Logout
  // ============================
  logout(): void {
    const token = localStorage.getItem('access_token');
    if (!token) {
      this.router.navigate(['/login']);
      return;
    }

    // Cabeçalho com HttpHeaders do Angular
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    // Chamada para o backend
    this.apiService.post('/auth/logout', {}, headers)
      .subscribe({
        next: () => {
          localStorage.removeItem('access_token');
          this.router.navigate(['/login']);
        },
        error: (err: any) => {
          console.warn('Erro ao invalidar token:', err);
          localStorage.removeItem('access_token');
          this.router.navigate(['/login']);
        }
      });
  }
}
