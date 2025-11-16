import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
// 1. Importe o Router e o NavigationEnd
import { Router, NavigationEnd, RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { filter } from 'rxjs/operators';



// Angular Material
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTabNavPanel, MatTabsModule } from '@angular/material/tabs';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';

import { ApiService } from './api';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    MatToolbarModule,
    MatTabsModule,
    MatIconModule,
    MatButtonModule,
    MatMenuModule,


  ],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App implements OnInit {
  protected readonly title = signal('metalyse-app');

 
  protected readonly mostrarMenu = signal(true);

  private rotasEscondidas = ['/login', '/cadastro', '/definir-senha'];
tabPanel: MatTabNavPanel|undefined;

  // 6. Injete o Router e adicione a lógica
  constructor(
    private apiService: ApiService,
    private router: Router // <-- Injete o Router
  ) {

    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      
      const urlAtual = event.urlAfterRedirects || event.url;
      const deveEsconder = this.rotasEscondidas.some(rota => urlAtual.includes(rota));
      
      // Atualiza o signal
      this.mostrarMenu.set(!deveEsconder);
    });
  }

  ngOnInit(): void {
    this.apiService.checkStatus().subscribe({
      next: () => console.log('✅ Backend Python (API) está Online!'),
      error: () => console.error('❌ ERRO: Não foi possível conectar ao backend Python.')
    });
  }
}