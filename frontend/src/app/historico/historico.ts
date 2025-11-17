import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';

// Módulos do Angular Material
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';

export interface HistoricoItem {
  nomeArquivo: string;
  formato: string;
  dataAnalise: string;
  horaAnalise: string;
}


const ELEMENT_DATA: HistoricoItem[] = [
  { nomeArquivo: 'relatorio_caso_2023.pdf', formato: 'PDF', dataAnalise: '25/10/2023', horaAnalise: '14:30:15' },
  { nomeArquivo: 'colecao_images_projetoX.zip', formato: 'ZIP', dataAnalise: '25/10/2023', horaAnalise: '12:15:00' },
  { nomeArquivo: 'dados_financeiros.zip', formato: 'CSV', dataAnalise: '25/10/2023', horaAnalise: '10:12:05' },
  { nomeArquivo: 'gravacao_audio_suspeito.mp3', formato: 'MP3', dataAnalise: '24/10/2023', horaAnalise: '08:57:41' },
  { nomeArquivo: 'log_servidor.txt', formato: 'TXT', dataAnalise: '24/10/2023', horaAnalise: '09:00:17' },
  { nomeArquivo: 'documento_confidencial.docx', formato: 'DOCX', dataAnalise: '23/10/2023', horaAnalise: '17:45:22' },
  { nomeArquivo: 'backup_sistema.sql', formato: 'SQL', dataAnalise: '23/10/2023', horaAnalise: '11:20:30' },
];

@Component({
  selector: 'app-historico',
  standalone: true,
  imports: [
    CommonModule,
   
    MatCardModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatButtonModule,
    MatMenuModule,
    MatTableModule,
    MatPaginatorModule
  ],
  templateUrl: './historico.html',
  styleUrls: ['./historico.css']
})
export class Histori implements AfterViewInit {
  

  displayedColumns: string[] = ['nomeArquivo', 'formato', 'dataAnalise', 'horaAnalise'];
  dataSource = new MatTableDataSource<HistoricoItem>(ELEMENT_DATA);


  @ViewChild(MatPaginator) paginator!: MatPaginator;

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
}