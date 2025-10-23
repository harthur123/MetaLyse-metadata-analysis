// ARQUIVO: src/app/cadastro/cadastro.ts

import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms'; 
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { RouterLink } from '@angular/router'; 

@Component({
  selector: 'app-cadastro',
  standalone: true,
  imports: [
    FormsModule, 
    MatCardModule, 
    MatInputModule, 
    MatFormFieldModule, 
    MatButtonModule,
    RouterLink
  ],
  templateUrl: './cadastro.html', 
  styleUrl: './cadastro.css'      
})
export class Cadastro {
  nome = '';
  email = '';
  senha = '';

  onCadastro() {
    console.log('Tentativa de Cadastro:', this.email);
   
  }
}