import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FoodMenuComponent } from './food-menu.component';

describe(' FoodMenuComponent', () => {
  let component:  FoodMenuComponent;
  let fixture: ComponentFixture< FoodMenuComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FoodMenuComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent( FoodMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
