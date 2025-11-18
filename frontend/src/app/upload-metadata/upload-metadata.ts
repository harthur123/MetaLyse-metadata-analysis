import { Component } from '@angular/core';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { MatIcon, MatIconModule } from "@angular/material/icon";
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatProgressBarModule } from '@angular/material/progress-bar';


@Component({
  selector: 'app-upload-metadata',
  templateUrl: './upload-metadata.html',
  styleUrls: ['./upload-metadata.css'],
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatProgressBarModule]
})
export class UploadMetadata {

  selectedFile: File | null = null;
  previewUrl: string | null = null;
  safePdfUrl: SafeResourceUrl | null = null;

  metadata: any = null;
  extractedMetadata: any = null;

  fileType: 'pdf' | 'jpeg' | null = null;

  uploading: boolean = false;
  uploadProgress: number = 0;

  isDragging: boolean = false;

  errorMessage: string = '';

  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {}

  // =========================
  // Seleção de arquivo
  // =========================
  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (!file) return;

    this.handleFile(file);
  }

  // Drag & Drop
  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;

    const file = event.dataTransfer?.files[0];
    if (file) this.handleFile(file);
  }

  private handleFile(file: File): void {
    this.selectedFile = file;
    this.fileType = null;
    this.previewUrl = null;
    this.safePdfUrl = null;
    this.metadata = null;
    this.extractedMetadata = null;
    this.errorMessage = '';

    // detecta tipo do arquivo
    if (file.type === 'application/pdf') this.fileType = 'pdf';
    else if (file.type === 'image/jpeg') this.fileType = 'jpeg';
    else {
      this.errorMessage = 'Apenas PDF ou JPEG são suportados!';
      return;
    }

    // gera preview
    const url = URL.createObjectURL(file);

    if (this.fileType === 'pdf') {
      this.safePdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
    } else if (this.fileType === 'jpeg') {
      this.previewUrl = url;
    }
  }

  // =========================
  // Envio ao backend
  // =========================
 // =========================
  // Envio ao backend (COM TOKEN MANUAL)
  // =========================
  uploadFile(): void {
    if (!this.selectedFile) return;

    this.uploading = true;
    this.uploadProgress = 0;

    // 1. Pega o token manualmente do armazenamento
    const token = localStorage.getItem('access_token');
    console.log('🔑 Token lido no componente:', token); 

    // 2. Cria o cabeçalho manualmente (PRECISA IMPORTAR HttpHeaders lá em cima!)
    let headers = new HttpHeaders();
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    // 3. Envia a requisição PASSANDO O HEADER EXPLICITAMENTE
    this.http.post('http://127.0.0.1:5000/api/metadata/upload', formData, {
      headers: headers, 
      reportProgress: true,
      observe: 'events'
    }).subscribe({
      next: (event: any) => {
        if (event.type === 1 && event.total) {
          this.uploadProgress = Math.round((event.loaded / event.total) * 100);
        }

        if (event.body) {
          console.log('✅ Sucesso:', event.body);
          // Ajuste aqui para bater com o JSON do backend:
          this.metadata = event.body.file; // Dados do arquivo (tamanho, nome)
          this.extractedMetadata = event.body.metadados_extraidos; // Dados do Exif/PDF
          this.uploading = false;
        }
      },
      error: (err) => {
        console.error('❌ Erro no upload:', err);
        this.errorMessage = err.error?.msg || 'Erro ao processar arquivo.';
        this.uploading = false;
      }
    });
  }

  // =========================
  // HELPERS (As funções que estavam faltando!)
  // =========================
  
  isImageFile(): boolean {
    // Verifica se é imagem (backend retorna jpeg ou jpg)
    return this.fileType === 'jpeg' || (this.selectedFile?.type === 'image/jpeg');
  }

  isPdfFile(): boolean {
    return this.fileType === 'pdf' || (this.selectedFile?.type === 'application/pdf');
  }
}
