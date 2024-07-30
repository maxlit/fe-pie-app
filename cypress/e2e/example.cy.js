describe('Visit langtools and interact', () => {
  it('clicks on the button and checks field values', () => {
    cy.visit('/pie');
    //cy.get('#example-btn-1').click();

    cy.wait(1000); // wait for any updates

    cy.get('body').then(() => {
      const sBtn = Cypress.$('#search-btn').val();
      const rBtn = Cypress.$('#random-btn').val();

      // Use custom task to log to the terminal
      cy.task('log', `sBtn Value: ${sBtn}`);
      cy.task('log', `rBtn Value: ${rBtn}`);

      expect(sBtn !== '' || rBtn !== '', 'At least one field should have a value').to.be.true;
    });
  });
});
