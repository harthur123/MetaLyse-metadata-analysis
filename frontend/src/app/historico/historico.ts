import { Component, AfterViewInit, ViewChild, inject } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
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
    MatNativeDateModule,
    DatePipe
  ],
  templateUrl: './historico.html',
  styleUrls: ['./historico.css']
})
export class Historico implements AfterViewInit {
  private http = inject(HttpClient);

  displayedColumns: string[] = ['nome_arquivo', 'formato', 'data_analise', 'hora_analise'];

  dataSource = new MatTableDataSource<HistoricoItem>([]);

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor() {
    // Configura o filtro corretamente
    this.dataSource.filterPredicate = (data: HistoricoItem, filter: string) => {
      const f = filter.trim().toLowerCase();
      return (
        data.nome_arquivo.toLowerCase().includes(f) ||
        data.formato.toLowerCase().includes(f) ||
        data.data_analise.toLowerCase().includes(f) ||
        data.hora_analise.toLowerCase().includes(f)
      );
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

    this.http.get<any>('http://127.0.0.1:5000/api/history/me', { headers }).subscribe({
      next: (res) => {
        console.log("Histórico carregado:", res);
        this.dataSource.data = res.history || res || [];
      },
      error: (err) => {
        console.error("❌ Erro ao carregar histórico:", err);
      }
    });
  }
}
     