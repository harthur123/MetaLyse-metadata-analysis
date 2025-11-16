import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { MatIcon, MatIconModule } from "@angular/material/icon";
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatProgressBarModule } from '@angular/material/progress-bar';

@Component({
  selector: 'app-upload-metadata',
  templateUrl: './upload-metadata.html',
  styleUrls: ['./upload-metadata.css'],
  imports: [CommonModule,
    FormsModule,
    HttpClientModule,
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
  uploadFile(): void {
    if (!this.selectedFile) return;

    this.uploading = true;
    this.uploadProgress = 0;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post('http://127.0.0.1:5000/api/metadata/upload', formData, {
      reportProgress: true,
      observe: 'events'
    }).subscribe({
      next: (event: any) => {
        if (event.type === 1 && event.total) {
          // progresso
          this.uploadProgress = Math.round((event.loaded / event.total) * 100);
        }

        if (event.body) {
          // resposta final
          this.metadata = event.body.metadata;
          this.extractedMetadata = event.body.extracted;
          this.uploading = false;
        }
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = err.error?.msg || 'Erro ao processar arquivo.';
        this.uploading = false;
      }
    });
  }

  // helpers
  isImageFile(): boolean {
    return this.fileType === 'jpeg';
  }

  isPdfFile(): boolean {
    return this.fileType === 'pdf';
  }
}
