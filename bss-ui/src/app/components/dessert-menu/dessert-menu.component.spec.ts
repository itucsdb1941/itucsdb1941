import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DessertMenuComponent } from './dessert-menu.component';

describe(' DessertMenuComponent', () => {
  let component:  DessertMenuComponent;
  let fixture: ComponentFixture< DessertMenuComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DessertMenuComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent( DessertMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
