import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { ActivatedRoute, Router } from '@angular/router';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-definir-senha',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './definir-senha.html',
  styleUrls: ['./definir-senha.css'],
})
export class DefinirSenha {
  private http = inject(HttpClient);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  novaSenha = '';
  confirmarSenha = '';
  token = '';
  loading = false;
  errorMsg = '';
  successMsg = '';

  constructor() {
    // Captura o token da query string: /definir-senha?token=xxxx
    this.route.queryParams.subscribe(params => {
      this.token = params['token'] || '';
    });
  }

  definirSenha() {
    this.errorMsg = '';
    this.successMsg = '';

    if (!this.novaSenha || !this.confirmarSenha) {
      this.errorMsg = 'Preencha todos os campos.';
      return;
    }

    if (this.novaSenha !== this.confirmarSenha) {
      this.errorMsg = 'As senhas não coincidem.';
      return;
    }

    if (!this.token) {
      this.errorMsg = 'Token inválido ou ausente.';
      return;
    }

    this.loading = true;

    const body = { token: this.token, new_password: this.novaSenha };

    this.http.post('http://127.0.0.1:5000/api/auth/reset-password', body)
      .subscribe({
        next: () => {
          this.loading = false;
          this.successMsg = 'Senha definida com sucesso!';
          // Opcional: redirecionar para login
          setTimeout(() => this.router.navigate(['/login']), 2000);
        },
        error: (err) => {
          this.loading = false;
          this.errorMsg = err.error?.message || 'Erro ao redefinir a senha.';
        }
      });
  }
}
