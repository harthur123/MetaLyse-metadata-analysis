import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DefinirSenha } from './definir-senha';

describe('DefinirSenha', () => {
  let component: DefinirSenha;
  let fixture: ComponentFixture<DefinirSenha>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DefinirSenha]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DefinirSenha);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
