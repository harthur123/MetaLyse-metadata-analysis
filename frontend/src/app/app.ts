import { Component, OnInit, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { Router, NavigationEnd, RouterOutlet, RouterLink, RouterLinkActive, RouterModule } from '@angular/router';
import { filter } from 'rxjs/operators';

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

  private router = inject(Router);        // 🔥 INJEÇÃO CORRETA  
  private apiService = inject(ApiService);

  protected readonly title = signal('metalyse-app');
  protected readonly mostrarMenu = signal(true);

  private rotasEscondidas = ['/login', '/cadastro', '/definir-senha'];

  tabPanel: MatTabNavPanel | undefined;

  constructor() {
    // 🔥 Agora router existe porque usamos inject()
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe((event: any) => {

        const urlAtual = event.urlAfterRedirects || event.url;
        const deveEsconder = this.rotasEscondidas.some(rota => urlAtual.includes(rota));

        this.mostrarMenu.set(!deveEsconder);
      });
  }

  ngOnInit(): void {
    this.apiService.checkStatus().subscribe({
      next: () => console.log('✅ Backend Python está Online'),
      error: () => console.error('❌ Não foi possível conectar ao backend')
    });
  }
}
