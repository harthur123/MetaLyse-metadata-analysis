import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
// import { MatCardModule } from '@angular/material/card'; // <-- REMOVA
// import { MatButtonModule } from '@angular/material/button'; // <-- REMOVA
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';

@Component({
  selector: 'app-upload-metadata',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    // MatCardModule, // <-- REMOVA
    // MatButtonModule, // <-- REMOVA
    MatIconModule,
    MatProgressBarModule
  ],
  templateUrl: './upload-metadata.html',
  styleUrls: ['./upload-metadata.css']
})
export class UploadMetadata {
  // --- NENHUMA MUDANÇA NECESSÁRIA NO CORPO DA CLASSE ---
  // Toda a sua lógica de 'selectedFile', 'uploading', 'isDragging',
  // 'handleFile', 'uploadFile' e os métodos de drag/drop 
  // continuam exatamente os mesmos.

  selectedFile: File | null = null;
  metadata: any = null;
  uploadProgress = 0;
  uploading = false;
  previewUrl: string | ArrayBuffer | null = null;
  isDragging = false; 

  constructor(private http: HttpClient) {}

  isImageFile(): boolean {
    return !!this.selectedFile && this.selectedFile.type.startsWith('image/');
  }

  isPdfFile(): boolean {
    return !!this.selectedFile && this.selectedFile.type === 'application/pdf';
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  onFileSelected(event: Event): void {
    const element = event.currentTarget as HTMLInputElement;
    const files = element.files;
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  handleFile(file: File): void {
    this.selectedFile = file;
    this.metadata = null;
    this.uploadProgress = 0;
    this.previewUrl = null;

    if (this.selectedFile) {
      const reader = new FileReader();
      reader.onload = () => this.previewUrl = reader.result;
      if (this.isImageFile() || this.isPdfFile()) {
        reader.readAsDataURL(this.selectedFile);
      }
    }
  }

  uploadFile() {
    if (!this.selectedFile) return;
    const formData = new FormData();
    formData.append('file', this.selectedFile);
    this.uploading = true;
    this.http.post('http://127.0.0.1:5000/api/upload-metadata', formData, {
      reportProgress: true,
      observe: 'events'
    }).subscribe({
      next: (event: any) => {
        if (event.type === 1 && event.total) {
          this.uploadProgress = Math.round((event.loaded / event.total) * 100);
        }
        if (event.type === 4) {
          this.metadata = event.body.metadata;
          this.uploading = false;
        }
      },
      error: (err) => {
        alert('Erro ao enviar arquivo: ' + err.message);
        this.uploading = false;
      }
    });
  }
}