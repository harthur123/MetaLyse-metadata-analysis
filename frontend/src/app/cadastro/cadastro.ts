import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';

// Angular Material
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-cadastro',
  standalone: true,
  imports: [
    FormsModule, MatCardModule, MatInputModule,
    MatFormFieldModule, MatButtonModule,
    RouterLink, HttpClientModule
  ],
  templateUrl: './cadastro.html',
  styleUrls: ['./cadastro.css']
})
export class Cadastro {

  username = '';
  email = '';
  password = '';

  passwordErrors: string[] = [];
  strength = 0;
  strengthColor = 'red';

  constructor(private http: HttpClient, private router: Router) {}

  validatePassword() {
    const errors: string[] = [];

    if (this.password.length < 6)
      errors.push("A senha deve ter no mínimo 6 caracteres.");
    if (!/[A-Z]/.test(this.password))
      errors.push("A senha deve conter pelo menos uma letra maiúscula.");
    if (!/[a-z]/.test(this.password))
      errors.push("A senha deve conter pelo menos uma letra minúscula.");
    if (!/[0-9]/.test(this.password))
      errors.push("A senha deve conter pelo menos um número.");
    if (!/[!@#$%^&*(),.?\":{}|<>]/.test(this.password))
      errors.push("A senha deve conter pelo menos um caractere especial (!@#$...).");
    if (/\s/.test(this.password))
      errors.push("A senha não pode conter espaços.");

    this.passwordErrors = errors;

    // força da senha (0 a 100%)
    let points = 0;
    if (this.password.length >= 6) points += 20;
    if (/[A-Z]/.test(this.password)) points += 20;
    if (/[a-z]/.test(this.password)) points += 20;
    if (/[0-9]/.test(this.password)) points += 20;
    if (/[!@#$%^&*(),.?\":{}|<>]/.test(this.password)) points += 20;

    this.strength = points;

    if (points <= 40) this.strengthColor = 'red';
    else if (points <= 80) this.strengthColor = 'orange';
    else this.strengthColor = 'green';
  }

  onCadastro() {
    if (this.passwordErrors.length > 0) {
      alert("A senha não atende aos requisitos.");
      return;
    }

    const usuario = {
      username: this.username,
      email: this.email,
      password: this.password
    };

    this.http.post('http://127.0.0.1:5000/api/register', usuario)
      .subscribe({
        next: () => {
          alert('Cadastro realizado com sucesso!');
          this.router.navigate(['/login']);
        },
        error: (err) =>
          alert(err.error?.message || 'Erro ao cadastrar.')
      });
  }
}
