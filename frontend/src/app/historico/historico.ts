import { Component, AfterViewInit, ViewChild, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

// Angular Material
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatMenuModule } from "@angular/material/menu";
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';

export interface HistoricoItem {
  nome_arquivo: string;
  formato: string;
  data_analise: string;
  hora_analise: string;
  // Novos campos opcionais para o Admin
  author_name?: string;
  author_email?: string;
}

@Component({
  selector: 'app-historico',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    MatCardModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatTableModule,
    MatPaginatorModule,
    MatMenuModule,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  templateUrl: './historico.html',
  styleUrls: ['./historico.css']
})
export class Historico implements AfterViewInit {
  private http = inject(HttpClient);

  // Colunas padrão
  displayedColumns: string[] = ['nome_arquivo', 'formato', 'data_analise', 'hora_analise'];
  
  dataSource = new MatTableDataSource<HistoricoItem>([]);
  isAdmin: boolean = false;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor() {
    // 1. Verifica se é Admin baseado no localStorage (salvo no login)
    const role = localStorage.getItem('user_role');
    this.isAdmin = (role === 'admin');

    // 2. Se for admin, adiciona a coluna 'usuario' na visualização
    if (this.isAdmin) {
      // Insere 'usuario' na segunda posição do array
      this.displayedColumns.splice(1, 0, 'usuario');
    }

    // 3. Configura o filtro (CORREÇÃO AQUI)
    // Forçamos o retorno a ser estritamente boolean
    this.dataSource.filterPredicate = (data: HistoricoItem, filter: string): boolean => {
      const f = filter.trim().toLowerCase();

      // Tratamento seguro: se o campo for undefined, usa string vazia ('')
      const nome = (data.nome_arquivo ?? '').toLowerCase();
      const formato = (data.formato ?? '').toLowerCase();
      const author = (data.author_name ?? '').toLowerCase();
      const email = (data.author_email ?? '').toLowerCase();
      const dataStr = (data.data_analise ?? '').toLowerCase();

      // Verifica se o termo existe em algum dos campos
      return nome.includes(f) ||
             formato.includes(f) ||
             author.includes(f) ||
             email.includes(f) ||
             dataStr.includes(f);
    };
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.loadHistory();
  }

  applyFilter(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.dataSource.filter = value.trim().toLowerCase();
  }

  loadHistory() {
    const token = localStorage.getItem('access_token');
    if (!token) {
      console.warn("⚠ Nenhum token encontrado no localStorage.");
      return;
    }

    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    // 4. Define a rota baseada no perfil
    const endpoint = this.isAdmin 
      ? 'http://127.0.0.1:5000/api/history/all' 
      : 'http://127.0.0.1:5000/api/history/me';

    this.http.get<any[]>(endpoint, { headers }).subscribe({
      next: (res) => {
        console.log("Histórico carregado (Bruto):", res);
        
        // 5. Mapeia os dados do Python para a Interface do Angular
        const formattedData: HistoricoItem[] = res.map((item: any) => {
            const dataObj = new Date(item.created_at);
            
            return {
                nome_arquivo: item.filename,
                formato: item.filetype,
                // Formata Data e Hora separadas para exibir na tabela
                data_analise: dataObj.toLocaleDateString('pt-BR'),
                hora_analise: dataObj.toLocaleTimeString('pt-BR', {hour: '2-digit', minute:'2-digit'}),
                // Campos extras (Admin)
                author_name: item.author_name,
                author_email: item.author_email
            };
        });

        this.dataSource.data = formattedData;
      },
      error: (err) => {
        console.error("❌ Erro ao carregar histórico:", err);
      }
    });
  }
}