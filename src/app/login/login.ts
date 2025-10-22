// ARQUIVO: src/app/login/login.ts

import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms'; // Módulo para [(ngModel)]
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { RouterLink } from '@angular/router'; // Mantido para futuras rotas

@Component({
  selector: 'app-login', // <--- Seletor usado em app.html
  standalone: true,
  imports: [
    FormsModule, 
    MatCardModule, 
    MatInputModule, 
    MatFormFieldModule, 
    MatButtonModule,
    RouterLink
  ],
  templateUrl: './login.html', 
  styleUrl: './login.css'      
})
export class Login { // Nome da classe
  username = '';
  password = '';

  onLogin() {
    console.log('Tentativa de Login:', this.username);
    // Lógica para enviar dados ao ApiService
  }
}